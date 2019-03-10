from flask import request, jsonify

from . import controllers

from uber_sante.utils import json_helper as js

from uber_sante.services.booking_service import BookingService
from uber_sante.services.availability_service import AvailabilityService

from uber_sante.miscellaneous.observable import *

@controllers.route('/availability', methods=['GET', 'PUT', 'DELETE'])
def availability():

    if request.method == 'PUT':
        # example use case: Make doctor availability
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure

        doctor_id = request.args.get('doctor_id')
        start = request.args.get('start')
        room = request.args.get('room')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        booking_type = request.args.get('booking_type')

        if doctor_id is None:
            return js.create_json(data=None, message="No doctor id provided",  return_code=js.ResponseReturnCode.CODE_400)
        if start is None:
            return js.create_json(data=None, message="No start time provided",  return_code=js.ResponseReturnCode.CODE_400)
        if room is None:
            return js.create_json(data=None, message="No room number provided",  return_code=js.ResponseReturnCode.CODE_400)
        if year is None:
            return js.create_json(data=None, message="No year provided",  return_code=js.ResponseReturnCode.CODE_400)
        if month is None:
            return js.create_json(data=None, message="No month provided",  return_code=js.ResponseReturnCode.CODE_400)
        if day is None:
            return js.create_json(data=None, message="No day provided",  return_code=js.ResponseReturnCode.CODE_400)
        if booking_type is None:
            return js.create_json(data=None, message="No booking type provided",  return_code=js.ResponseReturnCode.CODE_400)

        result = AvailabilityService().create_availability(doctor_id, start, room, '1', year, month, day, booking_type)

        return js.create_json(data=[result], message="Availability record created",  return_code=js.ResponseReturnCode.CODE_201)

        
    if request.method == 'DELETE':
        # example use case: delete doctor availability
        # params: appointment_id (int, required)
        # return: success/failure message

        availability_id = request.args.get('id')
        
        if availability_id is None:
            return js.create_json(data=None, message="No availability id provided",  return_code=js.ResponseReturnCode.CODE_400)

        availability_result = AvailabilityService().get_availability(availability_id)

        if availability_result == False:
            return js.create_json(data=None, message="Doctor availability does not exist",  return_code=js.ResponseReturnCode.CODE_400)

        is_free = availability_result.free
        result = None

        if is_free:
            result = AvailabilityService().cancel_availability(availability_id)
        else:
            patient_id = BookingService().get_patient_id_from_availability_id(availability_id)
            bookingResult = BookingService().cancel_booking_with_availability(availability_id)

            if bookingResult:
                res = AvailabilityService().cancel_availability(availability_id)
                if res:
                    # observer design pattern hook #
                    notifier.attach({patient_id: availability_result})

            else:
                return js.create_json(data=None, message="Could not delete doctor availability",  return_code=js.ResponseReturnCode.CODE_500)
    
        return js.create_json(data=None, message="Successfully deleted doctor availability",  return_code=js.ResponseReturnCode.CODE_200)

