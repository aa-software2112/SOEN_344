from flask import request, jsonify

from . import controllers
from uber_sante.utils import json_helper as js
from uber_sante.services.availability_service import AvailabilityService


@controllers.route('/availability', methods=['GET', 'PUT', 'DELETE'])
def availability():

    if request.method == 'PUT':
        # example use case: Make doctor availability
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure
        # TODO: implement patient cache to retrieve the appointment from the patient cache (line 48, 49)
        # TODO: connect the call to the scheduler class to try reserving the availability (line 51)
        # TODO: connect the call to the booking_service to create the booking in the Booking table (line 54)

        doctor_id = request.get_json().get('doctor_id')
        start = request.get_json().get('start')
        room = request.get_json().get('room')
        year = request.get_json().get('year')
        month = request.get_json().get('month')
        day = request.get_json().get('day')
        booking_type = request.get_json().get('booking_type')

        result = AvailabilityService().create_availability(doctor_id, start, room, '1', year, month, day, booking_type)

        return js.create_json(data=[result], message="Availability record created",  return_code=js.ResponseReturnCode.CODE_201)
