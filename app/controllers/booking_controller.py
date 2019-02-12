import os
from . import controllers
from cache import get_from_cache, set_to_cache
from config import Config
from app.utils.dbutil import DBUtil
from flask import Flask, request, jsonify, render_template

app = Flask('app')
Config.DATABASE = os.path.join(app.root_path + '/db/', 'database.db')
app.config.from_object(Config)
db = DBUtil(app, False).get_instance(False)

@controllers.route('/booking', methods=['GET', 'PUT', 'DELETE'])
def book():
    if request.method == 'GET':
        patient_id = request.args.get('patient_id')
        doctor_id = request.args.get('doctor_id')

        if patient_id is None and doctor_id is None:
            return jsonify('No booking parameters specified'), 400
        
        results = True # booking_service.get_booking(patient_id, doctor_id)

        return jsonify(results), 200

    if request.method == 'PUT':
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
            True # appointment_service.book(result, patient)
        else:
            return jsonify('Appointment slot already booked'), 403

        return jsonify('Appointment successfully booked'), 200
    
    if request.method == 'DELETE':
        availability_id = request.args.get('availability_id')
        
        if availability_id is None:
            return jsonify('No booking specified'), 400
        
        result = True # scheduler.free_booking(availability_id) # returns true or false

        if result:
            True # booking_service.delete_booking(availability_id)
        else:
            jsonify('Unable to delete booking'), 400
        
        jsonify('Booking deleted'), 200
