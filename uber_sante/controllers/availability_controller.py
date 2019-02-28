from . import controllers
from uber_sante.services.availability_service import AvailabilityService
from flask import request, jsonify
from uber_sante.utils import json_helper as js


@controllers.route('/availability', methods=['GET', 'PUT', 'DELETE'])
def availability():

    if request.method == 'PUT':
        # example use case: Make doctor availability
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure
        # TODO: implement patient cache to retrieve the appointment from the patient cache (line 48, 49)
        # TODO: connect the call to the scheduler class to try reserving the availability (line 51)
        # TODO: connect the call to the booking_service to create the booking in the Booking table (line 54)

        doctor_id = request.args.get('doctor_id')
        start = request.args.get('start')
        room = request.args.get('room')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        booking_type = request.args.get('booking_type')

        result = AvailabilityService().create_availability(doctor_id, start, room, '1', year, month, day, booking_type)

        return js.create_json(data=[result], message="Availability record created",  return_code=js.ResponseReturnCode.CODE_201)
