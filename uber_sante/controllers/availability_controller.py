from flask import request, jsonify

from . import controllers

from uber_sante.utils import json_helper as js

from uber_sante.services.booking_service import BookingService
from uber_sante.services.availability_service import AvailabilityService

@controllers.route('/availability', methods=['GET', 'PUT', 'DELETE'])
def availability():

    if request.method == 'PUT':
        # example use case: Make doctor availability
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure

        doctor_id = request.get_json().get('doctor_id')
        start = request.get_json().get('start')
        room = request.get_json().get('room')
        year = request.get_json().get('year')
        month = request.get_json().get('month')
        day = request.get_json().get('day')
        booking_type = request.get_json().get('booking_type')

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

            availability_id = request.get_json().get('id')
            
            if availability_id is None:
                    return js.create_json(data=None, message="No availability id provided",  return_code=js.ResponseReturnCode.CODE_400)

            result = None
            is_free = AvailabilityService().get_availability(availability_id).free

            if is_free:
                    result = AvailabilityService().cancel_availability(availability_id)
            else:
                    bookingResult = BookingService().cancel_booking(availability_id)

                    if bookingResult:
                            AvailabilityService().cancel_availability(availability_id)
                    else:
                            return js.create_json(data=None, message="Cannot delete doctor availability",  return_code=js.ResponseReturnCode.CODE_500)
     
            return js.create_json(data=None, message="Successfully deleted doctor availability",  return_code=js.ResponseReturnCode.CODE_200)

