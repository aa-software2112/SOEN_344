from flask import request, jsonify

from . import controllers

from uber_sante.utils import json_helper as js
from uber_sante.utils.room_formatter import FormatRoom

from uber_sante.models.scheduler import AppointmentRequestType

from uber_sante.services.booking_service import BookingService
from uber_sante.services.availability_service import AvailabilityService, AvailabilityStatus

format_room = FormatRoom()
booking_service = BookingService()
availability_service = AvailabilityService()


@controllers.route('/availability', methods=['GET', 'PUT', 'DELETE'])
def availability():
    if request.method == 'GET':
        # example use case: Make doctor availability
        # params: doctor_id (int, required, from cookie)
        # return: availability object(s)

        availability_id = request.args.get('availability_id')
        doctor_id = request.args.get('doctor_id')

        if doctor_id is None and availability_id is None:
            result = availability_service.get_all_availabilities()

            if result == AvailabilityStatus.NO_AVAILABILITIES:
                return js.create_json(data=None, message="No availabilites", return_code=js.ResponseReturnCode.CODE_200)

            return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

        result = None

        if doctor_id is not None:
            result = availability_service.get_availability_by_doctor_id(doctor_id)
        else:
            result = availability_service.get_availability(availability_id)

        if result is None:
            return js.create_json(data=None, message="Could not retrieve availabilities", return_code=js.ResponseReturnCode.CODE_500)
        if result == AvailabilityStatus.NO_AVAILABILITIES:
            return js.create_json(data=None, message="Doctor does not have any availabilites", return_code=js.ResponseReturnCode.CODE_200)

        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

    if request.method == 'PUT':
        # example use case: Make doctor availability
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure

        doctor_id = request.get_json().get('doctor_id')
        start = request.get_json().get('start')
        room = request.get_json().get('room')
        year = request.get_json().get('year')
        month = request.get_json().get('month').lstrip("0")
        day = request.get_json().get('day').lstrip("0")

        booking_type = request.get_json().get('booking_type')

        if doctor_id is None:
            return js.create_json(data=None, message="No doctor id provided", return_code=js.ResponseReturnCode.CODE_400)
        if start is None:
            return js.create_json(data=None, message="No start time provided", return_code=js.ResponseReturnCode.CODE_400)
        if room is None:
            return js.create_json(data=None, message="No room number provided", return_code=js.ResponseReturnCode.CODE_400)
        if year is None:
            return js.create_json(data=None, message="No year provided", return_code=js.ResponseReturnCode.CODE_400)
        if month is None:
            return js.create_json(data=None, message="No month provided", return_code=js.ResponseReturnCode.CODE_400)
        if day is None:
            return js.create_json(data=None, message="No day provided", return_code=js.ResponseReturnCode.CODE_400)
        if booking_type is None:
            return js.create_json(data=None, message="No booking type provided", return_code=js.ResponseReturnCode.CODE_400)

        result = None

        if booking_type == AppointmentRequestType.WALKIN:
            result = availability_service.check_and_create_availability_walkin(doctor_id, start, room, '1', year, month, day, booking_type)

        if booking_type == AppointmentRequestType.ANNUAL:
            result = availability_service.check_and_create_availability_annual(doctor_id, start, room, '1', year, month, day, booking_type)

        if result == AvailabilityStatus.NO_AVAILABILITIES:
            return js.create_json(data=None, message="No rooms available at this time slot", return_code=js.ResponseReturnCode.CODE_400)
        if result == AvailabilityStatus.AVAILABILITY_ALREADY_BOOKED_AT_THIS_TIME:
            return js.create_json(data=None, message="Doctor already has a room booked at this time slot", return_code=js.ResponseReturnCode.CODE_400)

        return js.create_json(data=[result], message="Availability record created", return_code=js.ResponseReturnCode.CODE_201)

    if request.method == 'DELETE':
        # example use case: delete doctor availability
        # params: appointment_id (int, required)
        # return: success/failure message

        availability_id = request.get_json().get('id')

        if availability_id is None:
            return js.create_json(data=None, message="No availability id provided", return_code=js.ResponseReturnCode.CODE_400)

        availability_result = availability_service.get_availability(availability_id)

        if availability_result == False:
            return js.create_json(data=None, message="Doctor availability does not exist", return_code=js.ResponseReturnCode.CODE_400)

        is_free = availability_result.free
        result = None

        if is_free:
            result = availability_service.cancel_availability(availability_id)
        else:
            bookingResult = BookingService().cancel_booking_with_availability(availability_id)

            if bookingResult:
                availability_service.cancel_availability(availability_id)
            else:
                return js.create_json(data=None, message="Could not delete doctor availability", return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=None, message="Successfully deleted doctor availability", return_code=js.ResponseReturnCode.CODE_200)


@controllers.route('/availability/<string:availability_id>', methods=['PUT'])
def modify_availability(availability_id):
    """ Makes a new availability and deletes the old one, which is used to generate a new availability_id
    This is so that a patient who tries to book the previous availability_id won't be able to """
    if request.method == 'PUT':
        doctor_id = request.get_json().get('doctor_id')
        start = request.get_json().get('start')
        room = request.get_json().get('room')
        year = request.get_json().get('year')
        month = request.get_json().get('month').lstrip("0")
        day = request.get_json().get('day').lstrip("0")

        current_availability = availability_service.get_availability(availability_id)
        booking_type = current_availability.booking_type

        if doctor_id is None:
            doctor_id = current_availability.doctor_id
        if start is None or not start:
            start = str(current_availability.start)
        if room is None or not room:
            room = current_availability.room
        if year is None or not year:
            year = str(current_availability.year)
        if month is None or not month:
            month = str(current_availability.month)
        if day is None or not day:
            day = str(current_availability.day)

        if availability_service.room_is_available_at_this_time(start, room, year, month, day, doctor_id) == AvailabilityStatus.NO_ROOMS_AT_THIS_TIME:
            return js.create_json(data=None, message="Room not available at this time.", return_code=js.ResponseReturnCode.CODE_400)

        else:
            # Make a new availability
            if booking_type == AppointmentRequestType.WALKIN:
                result = availability_service.check_and_create_availability_walkin(doctor_id, start, room, '1', year, month, day, booking_type, availability_id)
            if booking_type == AppointmentRequestType.ANNUAL:
                result = availability_service.check_and_create_availability_annual(doctor_id, start, room, '1', year, month, day, booking_type, availability_id)

            if result == AvailabilityStatus.NO_AVAILABILITIES_AT_THIS_HOUR:
                return js.create_json(data=None, message="No rooms available at this time slot", return_code=js.ResponseReturnCode.CODE_400)

            # Delete the old availability and booking at this availability if there is one
            booking_service.cancel_booking_with_availability(availability_id)
            availability_service.cancel_availability(availability_id)

            return js.create_json(data=None, message="Availability successfully modified", return_code=js.ResponseReturnCode.CODE_201)

@controllers.route('/availability/room-availability', methods=['GET'])
def get_available_rooms():

    if request.method == 'GET':

        start = request.args.get('start')
        year = request.args.get('year')
        month = request.args.get('month').lstrip("0")
        day = request.args.get('day').lstrip("0")

        if start is None:
            return js.create_json(data=None, message="No start time parameter provided", return_code=js.ResponseReturnCode.CODE_400)
        if year is None:
            return js.create_json(data=None, message="No year parameter provided", return_code=js.ResponseReturnCode.CODE_400)
        if month is None:
            return js.create_json(data=None, message="No month parameter provided", return_code=js.ResponseReturnCode.CODE_400)
        if day is None:
            return js.create_json(data=None, message="No day parameter provided", return_code=js.ResponseReturnCode.CODE_400)

        result = availability_service.get_available_rooms(start, year, month, day)

        if result is None:
            return js.create_json(data=None, message="Could not retrieve availabilities", return_code=js.ResponseReturnCode.CODE_500)
        if result == AvailabilityStatus.ALL_ROOMS_OPEN:
            return js.create_json(data=format_room.all_rooms, message=None, return_code=js.ResponseReturnCode.CODE_200)
        if result == AvailabilityStatus.NO_ROOMS_AT_THIS_TIME:
            return js.create_json(data={}, message="No rooms available at this time", return_code=js.ResponseReturnCode.CODE_200)
        9
        return js.create_json(data=format_room.negate_rooms(result), message=None, return_code=js.ResponseReturnCode.CODE_200)
