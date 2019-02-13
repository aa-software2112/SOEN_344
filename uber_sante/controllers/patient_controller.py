import os
from . import controllers
from uber_sante.models.patient import Patient
from cache import get_from_cache, set_to_cache
from flask import Flask, request, jsonify

@controllers.route('/patient', methods=['GET', 'PUT'])
def patient():

    if request.method == 'GET':
    # example use case: make appointment
    # params: patient_id (int, required)
    # return: patient object
    # TODO: connect the call to the patient_service (line 21)

        patient_id = request.args.get('patient_id')

        if patient_id is None:
            return jsonify('No patient id specified'), 400

        result = True # patient_service.get_patient(patient_id)

        return jsonify(result), 200

    if request.method == 'PUT':
    # example use case: register patient
    # params: patient(Patient object, required)
    # return: sucess/failure
    # TODO: connect the call to the patient_service to insert the patient to the Patient table (line 47)

        req = request.args.get('patient')

        if req is None:
            return jsonify('No patient provided'), 400

        patient = Patient(
            req.id,
            req.f_name,
            req.l_name,
            req.health_card_nb,
            req.date_of_birth,
            req.gender,
            req.phone_nb,
            req.address, 
            req.email
        )

        result = True # patient_service.put_patient(patient)

        return jsonify(result), 200
