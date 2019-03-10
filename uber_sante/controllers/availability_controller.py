from flask import request, jsonify

from . import controllers

from uber_sante.utils import json_helper as js
from uber_sante.utils.time_interpreter import TimeInterpreter

from uber_sante.models.scheduler import AppointmentRequestType

from uber_sante.services.booking_service import BookingService
from uber_sante.services.availability_service import AvailabilityService, AvailabilityStatus

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
            return js.create_json(data=None, message="No parameters provided",
                                  return_code=js.ResponseReturnCode.CODE_400)

        result = None

        if doctor_id is not None:
            result = availability_service.get_availability_by_doctor_id(doctor_id)
        else:
            result = availability_service.get_availability(availability_id)

        if result is None:
            return js.create_json(data=None, message="Could not retrieve availabilities",
                                  return_code=js.ResponseReturnCode.CODE_500)
        if result == AvailabilityStatus.NO_AVAILABILITIES_FOR_DOCTOR:
            return js.create_json(data=None, message="Doctor does not have any availabilites",
                                  return_code=js.ResponseReturnCode.CODE_200)

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
            return js.create_json(data=None, message="No doctor id provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if start is None:
            return js.create_json(data=None, message="No start time provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if room is None:
            return js.create_json(data=None, message="No room number provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if year is None:
            return js.create_json(data=None, message="No year provided", return_code=js.ResponseReturnCode.CODE_400)
        if month is None:
            return js.create_json(data=None, message="No month provided", return_code=js.ResponseReturnCode.CODE_400)
        if day is None:
            return js.create_json(data=None, message="No day provided", return_code=js.ResponseReturnCode.CODE_400)
        if booking_type is None:
            return js.create_json(data=None, message="No booking type provided",
                                  return_code=js.ResponseReturnCode.CODE_400)

        result = None

        if booking_type == AppointmentRequestType.WALKIN:
            result = availability_service.check_and_create_availability_walkin(doctor_id, start, room, '1', year, month,
                                                                               day, booking_type)

        if booking_type == AppointmentRequestType.ANNUAL:
            result = availability_service.check_and_create_availability_annual(doctor_id, start, room, '1', year, month,
                                                                               day, booking_type)

        if result == AvailabilityStatus.NO_AVAILABILITIES_AT_THIS_HOUR:
            return js.create_json(data=None, message="No rooms available at this time slot",
                                  return_code=js.ResponseReturnCode.CODE_400)

        return js.create_json(data=[result], message="Availability record created",
                              return_code=js.ResponseReturnCode.CODE_201)

    if request.method == 'DELETE':
        # example use case: delete doctor availability
        # params: appointment_id (int, required)
        # return: success/failure message

        availability_id = request.get_json().get('id')

        if availability_id is None:
            return js.create_json(data=None, message="No availability id provided",
                                  return_code=js.ResponseReturnCode.CODE_400)

        availability_result = availability_service.get_availability(availability_id)

        if availability_result == False:
            return js.create_json(data=None, message="Doctor availability does not exist",
                                  return_code=js.ResponseReturnCode.CODE_400)

        is_free = availability_result.free
        result = None

        if is_free:
            result = availability_service.cancel_availability(availability_id)
        else:
            bookingResult = BookingService().cancel_booking_with_availability(availability_id)

            if bookingResult:
                availability_service.cancel_availability(availability_id)
            else:
                return js.create_json(data=None, message="Could not delete doctor availability",
                                      return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=None, message="Successfully deleted doctor availability",
                              return_code=js.ResponseReturnCode.CODE_200)


@controllers.route('/availability/<string:availability_id>', methods=['PUT'])
def modify_availability(availability_id):
    """ Makes a new availability and deletes the old one, which is used to generate a new availability_id
    This is so that a patient who tries to book the previous availability_id won't be able to """

    doctor_id = request.get_json().get('doctor_id')
    start = request.get_json().get('start')
    room = request.get_json().get('room')
    year = request.get_json().get('year')
    month = request.get_json().get('month')
    day = request.get_json().get('day')
    booking_type = request.get_json().get('booking_type')
    x_time = True

    current = availability_service.get_availability(availability_id, convertTime=False)

    if doctor_id is None:
        doctor_id = current.doctor_id
    if start is None or not start:
        start = str(current.start)
        x_time = False
    if room is None or not room:
        room = current.room
    if year is None or not year:
        year = str(current.year)
    if month is None or not month:
        month = str(current.month)
    if day is None or not day:
        day = str(current.day)
    if booking_type is None or not booking_type:
        booking_type = current.booking_type

    if not availability_service.room_is_available_at_this_time(start, room, year, month, day):
        return js.create_json(data=None, message="Room not available at this time.",
                              return_code=js.ResponseReturnCode.CODE_500)


    else:
        # Make a new availability
        if booking_type == AppointmentRequestType.WALKIN:
            result = availability_service.check_and_create_availability_walkin(doctor_id, start, room, '1', year, month,
                                                                               day, booking_type, convertTime=x_time)
        if booking_type == AppointmentRequestType.ANNUAL:
            result = availability_service.check_and_create_availability_annual(doctor_id, start, room, '1', year, month,
                                                                               day, booking_type, convertTime=x_time)

        if result == AvailabilityStatus.NO_AVAILABILITIES_AT_THIS_HOUR:
            return js.create_json(data=None, message="No rooms available at this time slot",
                                  return_code=js.ResponseReturnCode.CODE_400)

        # Delete the old availability and booking at this availability if there is one
        booking_service.cancel_booking_with_availability(availability_id)
        availability_service.cancel_availability(availability_id)

        return js.create_json(data=None, message="Availability successfully modified",
                              return_code=js.ResponseReturnCode.CODE_201)


@controllers.route('/viewavailability', methods=['PUT'])
def view_availability():
    if request.method == 'PUT':

        doctor_id = request.get_json().get('doctor_id')

        if doctor_id is None:
            return js.create_json(data=None, message="No parameters provided",
                                  return_code=js.ResponseReturnCode.CODE_400)

        result = None

        result = availability_service.get_availability_by_doctor_id(doctor_id)

        if result is None:
            return js.create_json(data=None, message="Could not retrieve availabilities",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if result == AvailabilityStatus.NO_AVAILABILITIES_FOR_DOCTOR:
            return js.create_json(data=None, message="Doctor does not have any availabilites",
                                  return_code=js.ResponseReturnCode.CODE_200)

        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)
