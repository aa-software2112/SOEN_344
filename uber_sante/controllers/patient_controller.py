import os

from flask import make_response

from . import controllers
from uber_sante.models.patient import Patient
from uber_sante.services.patient_service import PatientService
from uber_sante.utils import cookie_helper
from flask import Flask, request, jsonify

patient_service = PatientService()

@controllers.route('/viewmycookie', methods=['GET'])
def viewCookie():

    return jsonify(request.cookies), 200

@controllers.route('/logout', methods=['GET'])
def logout():

    if request.method == 'GET':

        resp = jsonify(logout_message="Successfully logged out!")
        resp = cookie_helper.logout_user_cookie(resp)
        return resp, 200


@controllers.route('/login', methods=['POST', 'GET'])
def login():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return jsonify(login_message="Already logged in!"), 400

        health_card_nb = request.args.get('health_card_nb')

        password = request.args.get('password')

        # Validate the login information
        patient_id = patient_service.validate_login_info(health_card_nb, password)

        # There was no patient linked with the health card number and password
        if patient_id == -1:
            return jsonify(login_message="Invalid login information"), 400

        # Set patient in cache
        patient_service.test_and_set_patient_into_cache(patient_id)

        # Sets the cookie, and status of "logged in" for front-end functionality switches
        resp = jsonify(login_message="Logged in successfully")

        # set the cookie in the response object
        resp = cookie_helper.set_user_logged(resp, patient_id, cookie_helper.UserTypes.PATIENT.value)

        return resp, 200

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
