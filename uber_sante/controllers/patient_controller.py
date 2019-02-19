import os

from . import controllers
from uber_sante.utils import cookie_helper
from uber_sante.models.patient import Patient
from uber_sante.services.patient_service import PatientService

from flask import Flask, request, jsonify, make_response

patient_service = PatientService()


@controllers.route('/viewmycookie', methods=['GET'])
def view_cookie():

    return jsonify(request.cookies), 200


@controllers.route('/logout', methods=['GET'])
def logout():

    if request.method == 'GET':

        resp = jsonify(logout_message="Successfully logged out!")
        resp = cookie_helper.logout_user_cookie(resp)
        return resp, 200


@controllers.route('/login', methods=['POST'])
def login():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return jsonify(login_message="Already logged in!"), 400

        health_card_nb = request.args.get('health_card_nb')
        password = request.args.get('password')

        # Validate the login information
        patient_id = patient_service.validate_login_info(
            health_card_nb, password)

        # There was no patient linked with the health card number and password
        if patient_id == -1:
            return jsonify(login_message="Invalid login information"), 400

        # Set patient in cache
        patient_service.test_and_set_patient_into_cache(patient_id)

        # set the cookie in the response object
        resp = jsonify(login_message="Logged in successfully")
        resp = cookie_helper.set_user_logged(
            resp, patient_id, cookie_helper.UserTypes.PATIENT.value)

        return resp, 200


@controllers.route('/patient', methods=['GET', 'PUT'])
def patient():

    if request.method == 'GET':
        # params: patient_id (int, required)
        # return: patient object

        patient_id = request.args.get('patient_id')

        if patient_id is None:
            return jsonify(status='error', data=None, error={'code': 400, 'message': 'Patient Id is not specified'}), 400

        result = patient_service.get_patient(patient_id)

        if result is None:
            return jsonify(status='error', data=None, error={'code': 500, 'message': 'Could not retrieve patient'}), 500

        return jsonify(status="success", data=result.asdict(), message=None), 200

    if request.method == 'PUT':
        # params: [various, look below] (int or string, required)
        # return: sucess/failure

        if request.args is None:
            return jsonify(status='error', data=None, error={'code': 400, 'message': 'No patient information provided'}), 400

        health_card_nb = request.args.get('health_card_nb')
        date_of_birth = request.args.get('date_of_birth')
        gender = request.args.get('gender')
        phone_nb = request.args.get('phone_nb')
        home_address = request.args.get('home_address')
        email = request.args.get('email')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        password = request.args.get('password')

        result = patient_service.create_patient(
            health_card_nb,
            date_of_birth,
            gender,
            phone_nb,
            home_address,
            email,
            first_name,
            last_name,
            password
        )

        if result == -1:
            return jsonify(status='error', data=None, error={'code': 500, 'message': 'Health card number already registered'})

        if result == -2:
            return jsonify(status='error', data=None, error={'code': 500, 'message': 'Email address already registered'})

        return jsonify(status="success", data=None, message='Patient record created'), 201
