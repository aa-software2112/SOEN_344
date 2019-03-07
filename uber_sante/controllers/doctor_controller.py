from . import controllers
from uber_sante.services.doctor_service import DoctorService
from uber_sante.utils import json_helper as js
from uber_sante.utils import cookie_helper
from flask import Flask, request, jsonify, make_response
from uber_sante.utils.cache import get_from_cache, set_to_cache
from flask import request, jsonify

doctor_service = DoctorService()

@controllers.route('/loginDoctor', methods=['POST'])
def loginDoctor():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in!", return_code=js.ResponseReturnCode.CODE_400)

        if request.get_json() is None:
            return js.create_json(None, "No login information provided", js.ResponseReturnCode.CODE_400)

        physician_permit = request.get_json().get('physician_permit')
        password = request.get_json().get('password')

        # Validate the login information
        doctor_id = doctor_service.validate_login_info(
            physician_permit, password)

        # There was no doctor linked with the physician number and password
        if doctor_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        doctor_service.test_and_set_doctor_into_cache(doctor_id)

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(
            resp, doctor_id, cookie_helper.UserTypes.DOCTOR.value)

        return resp, js.ResponseReturnCode.CODE_200.value
from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache

from uber_sante.models.scheduler import Scheduler

from uber_sante.services.doctor_service import DoctorService

doctor_service = DoctorService()

@controllers.route('/doctor', methods=['GET', 'PUT', 'DELETE'])
def book():

    if request.method == 'GET':
        # params: id (int, semi-required), doctor_name (text, semi-required)
        # return: doctor object

        doctor_id = request.args.get('id')
        doctor__last_name = request.args.get('last_name')

        if doctor_id is None and doctor__last_name is None:
            return js.create_json(data=None, message='No doctor params specified', return_code=js.ResponseReturnCode.CODE400)

        result = None

        if doctor__last_name is not None:
            result = doctor_service.get_doctor_by_name(doctor__last_name)
        else:
            result = doctor_service.get_doctor(doctor_id)

        if result is None:
            return js.create_json(data=None, message='Could not retrieve doctor', return_code=js.ResponseReturnCode.CODE500)
        if result == 3:
            return js.create_json(data=None, message='Doctor Id does not exist', return_code=js.ResponseReturnCode.CODE400)
        if result == 4:
            return js.create_json(data=None, message='Doctor with last name ${doctor_last_name} does not exist', return_code=js.ResponseReturnCode.CODE400)
        
        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE200)



