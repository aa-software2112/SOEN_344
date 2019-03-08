from . import controllers
from uber_sante.services.nurse_service import NurseService
from uber_sante.utils import json_helper as js
from uber_sante.utils import cookie_helper
from flask import Flask, request, jsonify, make_response
from uber_sante.utils.cache import get_from_cache, set_to_cache

nurse_service = NurseService()

@controllers.route('/loginNurse', methods=['POST'])
def loginNurse():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in!", return_code=js.ResponseReturnCode.CODE_400)

        if request.get_json() is None:
            return js.create_json(None, "No login information provided", js.ResponseReturnCode.CODE_400)

        access_id = request.get_json().get('access_id')
        password = request.get_json().get('password')

        # Validate the login information
        nurse_id = nurse_service.validate_login_info(
            access_id, password)

        # There was no doctor linked with the physician number and password
        if nurse_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        nurse_service.test_and_set_nurse_into_cache(nurse_id)

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(
            resp, nurse_id, cookie_helper.UserTypes.NURSE.value)

        return resp, js.ResponseReturnCode.CODE_200.value

@controllers.route('/make-annual-appointment-nurse', methods=['PUT'])
def make_annual_appointment():

    if request.method == 'PUT':

        #if not cookie_helper.user_is_logged(request):
        #    return js.create_json(data=None, message="User is not logged", return_code=js.ResponseReturnCode.CODE_400)

        availability_id = int(request.args.get('availability_id'))
        patient_id = request.args.get('patient_id')

        patient_service.test_and_set_patient_into_cache(patient_id)
        patient = patient_service.get_patient(patient_id)
        availability = availability_service.get_availability(availability_id)

        result = patient.make_annual_appointment(availability)

        if result == MakeAnnualStatus.SUCCESS:
            return js.create_json(data=None, message="Successfully added annual appointment", return_code=js.ResponseReturnCode.CODE_200)

        elif result == MakeAnnualStatus.HAS_ANNUAL_APPOINTMENT:
            return js.create_json(data=None, message="Patient already has an annual appointment in cart", return_code=js.ResponseReturnCode.CODE_400)


@controllers.route('/make-walkin-appointment-nurse', methods=['PUT'])
def make_walkin_appointment():

    if request.method == 'PUT':

        #if not cookie_helper.user_is_logged(request):
        #    return js.create_json(data=None, message="User is not logged", return_code=js.ResponseReturnCode.CODE_400)

        availability_id = int(request.args.get('availability_id'))
        patient_id = request.args.get('patient_id')

        patient_service.test_and_set_patient_into_cache(patient_id)
        patient = patient_service.get_patient(patient_id)
        availability = availability_service.get_availability(availability_id)

        patient.make_walkin_appointment(availability)

        return js.create_json(data=None, message="Successfully added walkin appointment", return_code=js.ResponseReturnCode.CODE_200)