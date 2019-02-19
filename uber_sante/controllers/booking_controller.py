from . import controllers
from uber_sante.utils.cache import get_from_cache
from flask import request, jsonify

@controllers.route('/booking', methods=['GET', 'PUT', 'DELETE'])
def book():

    if request.method == 'GET':
    # example use case: get_bookings
    # params: patient_id (int, semi-required), doctor_id (int, semi-required)
    # return: booking(s) belonging to the patient or doctor
    # TODO: connect the call to the booking_service (line 28)

        patient_id = request.args.get('patient_id')
        doctor_id = request.args.get('doctor_id')

        if patient_id is None and doctor_id is None:
            return jsonify('No booking parameters specified'), 400
        
        results = True # booking_service.get_booking(patient_id, doctor_id)

        return jsonify(results), 200

    if request.method == 'PUT':
    # example use case: checkout_appointment
    # params: appointment_id (int, required, from cookie), patient_id(int, required)
    # return: success/failure
    # TODO: implement patient cache to retrieve the appointment from the patient cache (line 48, 49)
    # TODO: connect the call to the scheduler class to try reserving the availability (line 51)
    # TODO: connect the call to the booking_service to create the booking in the Booking table (line 54)

        appointment_id = request.args.get('appointment_id')
        patient_id = request.args.get('patient_id')

        if appointment_id is None:
            return jsonify('No appointment specified'), 400
        if patient_id is None:
            return jsonify('No patient specified'), 400

        patient = get_from_cache(patient_id) # get the patient from cache
        appointment = patient.cart[appointment_id] # somewhat of a placeholder for now, waiting for cart to be implemented

        result = True #scheduler.try_booking(appointment)   # make a call to the scheduler here
                                                            # returns availability object
        if result:
            True # booking_service.book(result, patient)
        else:
            return jsonify('Appointment slot already booked'), 403

        return jsonify('Appointment successfully booked'), 200

    if request.method == 'DELETE':
    # example use case: cancel_booking
    # params: availability_id (int, required)
    # return: success/failure
    # TODO: connect the call to the scheduler class to free the availability (line 72)
    # TODO: connect the call to the booking_service to delete the booking fromn the Booking table(line 75)

        availability_id = request.args.get('availability_id')
        
        if availability_id is None:
            return jsonify('No booking specified'), 400
        
        result = True # scheduler.free_booking(availability_id) # returns true or false

        if result:
            True # booking_service.delete_booking(availability_id)
        else:
            jsonify('Unable to delete booking'), 400
        
        jsonify('Booking deleted'), 200
