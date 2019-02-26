import os

from . import controllers
from uber_sante.utils import cookie_helper
from uber_sante.models.patient import Patient
from uber_sante.services.patient_service import PatientService
from uber_sante.utils.cache import get_from_cache
from uber_sante.services.patient_service import CreatePatientStatus
from uber_sante.utils import json_helper as js
from flask import Flask, request, jsonify, make_response
from uber_sante.utils import cookie_helper

patient_service = PatientService()


@controllers.route('/viewmycookie', methods=['GET'])
def view_cookie():

    return js.create_json(data=request.cookies, message="Here is your cookie",
                              return_code=js.ResponseReturnCode.CODE_200)


@controllers.route('/logout', methods=['GET'])
def logout():

    if request.method == 'GET':

        resp = js.create_json(data=None, message="Successfully logged out!",
                              return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.logout_user_cookie(resp)
        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/login', methods=['POST'])
def login():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in!", return_code=js.ResponseReturnCode.CODE_400)

        health_card_nb = request.args.get('health_card_nb')
        password = request.args.get('password')

        # Validate the login information
        patient_id = patient_service.validate_login_info(
            health_card_nb, password)

        # There was no patient linked with the health card number and password
        if patient_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        patient_service.test_and_set_patient_into_cache(patient_id)

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(
            resp, patient_id, cookie_helper.UserTypes.PATIENT.value)

        return resp, js.ResponseReturnCode.CODE_200.value

@controllers.route('/patient', methods=['GET', 'PUT', 'DELETE'])
def patient():

    if request.method == 'GET':
        # params: patient_id (int, required)
        # return: patient object

        patient_id = request.args.get('patient_id')

        if patient_id is None:
            return js.create_json(data=None, message="Patient Id is not specified", return_code=js.ResponseReturnCode.CODE_400)

        result = patient_service.get_patient(patient_id)

        if result is None:
            return js.create_json(data=None, message="Could not retrieve patient", return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

    if request.method == 'PUT':
        # params: [various, look below] (int or string, required)
        # return: sucess/failure

        if request.args is None:
            return js.create_json(None, "No patient information provided", js.ResponseReturnCode.CODE_400)

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

        if result == CreatePatientStatus.HEALTH_CARD_ALREADY_EXISTS:
            return js.create_json(None, "Health card number already registered", js.ResponseReturnCode.CODE_500)

        if result == CreatePatientStatus.EMAIL_ALREADY_EXISTS:
            return js.create_json(None, "Email address already registered", js.ResponseReturnCode.CODE_500)

        return js.create_json(None, "Patient record created", js.ResponseReturnCode.CODE_201)

    if request.method == 'DELETE':
    # example use case: remove appointment
    # params: patient_id (int, required), availability_id (int, required)
    # return: success/failure

        patient_id = request.args.get('patient_id')
        availability_id = request.args.get('availability_id')

        if availability_id is None:
            return js.create_json(data=None, message="No appointment specified", return_code=js.ResponseReturnCode.CODE_400)
        if patient_id is None:
            return js.create_json(data=None, message="No patient specified", return_code=js.ResponseReturnCode.CODE_400)

        patient = get_from_cache(patient_id)

        # TODO: this method will be changed with respect to the updated appointment object.
        result = patient.remove_from_cart(availability_id)

        if result is None:
            return js.create_json(data=None, message="Appointment not found/removed", return_code=js.ResponseReturnCode.CODE_400)

        return js.create_json(data=None, message="Appointment removed", return_code=js.ResponseReturnCode.CODE_200)