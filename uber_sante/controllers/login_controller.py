from . import controllers
from flask import Flask, request, jsonify, make_response

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.models.scheduler import Scheduler

from uber_sante.services.doctor_service import DoctorService
from uber_sante.services.admin_service import AdminService
from uber_sante.services.nurse_service import NurseService
from uber_sante.services.patient_service import PatientService

from uber_sante.miscellaneous.observer import *

admin_service = AdminService()
nurse_service = NurseService()
doctor_service = DoctorService()
patient_service = PatientService()

@controllers.route('/logout', methods=['GET'])
def logout():
    """
    Logout of ANY user type
    :return:
    """
    if request.method == 'GET':

        resp = js.create_json(data=None, message="Successfully logged out!", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.logout_user_cookie(resp)
        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/login/admin', methods=['POST'])
def login_admin():
    """
    The endpoint for logging in as an administrator;
    This is necessary in order to register a doctor or a nurse -
    only an admin can do this
    """

    if request.method == 'POST':

        # User is already logged in (regardless of login-type {patient, admin, nurse, doctor})
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in", return_code=js.ResponseReturnCode.CODE_400)

        email = request.get_json().get('email')
        password = request.get_json().get('password')

        admin_id = admin_service.validate_login_info(email, password)

        if admin_id == -1:
            return js.create_json(data=None, message="Incorrect Admin Login information", return_code=js.ResponseReturnCode.CODE_400)

        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, admin_id, cookie_helper.UserTypes.ADMIN.value)

        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/login/patient', methods=['POST', 'OPTIONS'])
def login_patient():

    # Grab the data from the post request
    if request.method == 'POST':

        # Check that the user is not already logged (users can login accross multiple PCs, however)
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in!", return_code=js.ResponseReturnCode.CODE_400)

        if request.get_json() is None:
            return js.create_json(None, "No login information provided", js.ResponseReturnCode.CODE_400)

        health_card_nb = request.get_json().get('health_card_nb')
        password = request.get_json().get('password')

        # Validate the login information
        patient_id = patient_service.validate_login_info(health_card_nb, password)

        # There was no patient linked with the health card number and password
        if patient_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        patient_service.test_and_set_patient_into_cache(patient_id)

        # observer pattern hook
        notifier.notify()

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, patient_id, cookie_helper.UserTypes.PATIENT.value)

        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/login/doctor', methods=['POST'])
def login_doctor():

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
        doctor_id = doctor_service.validate_login_info(physician_permit, password)

        # There was no doctor linked with the physician number and password
        if doctor_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        doctor_service.test_and_set_doctor_into_cache(doctor_id)

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, doctor_id, cookie_helper.UserTypes.DOCTOR.value)

        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/login/nurse', methods=['POST'])
def login_nurse():

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
        nurse_id = nurse_service.validate_login_info(access_id, password)

        # There was no doctor linked with the physician number and password
        if nurse_id == -1:
            return js.create_json(data=None, message="Invalid login information", return_code=js.ResponseReturnCode.CODE_400)

        # Set patient in cache
        nurse_service.test_and_set_nurse_into_cache(nurse_id)

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, nurse_id, cookie_helper.UserTypes.NURSE.value)

        return resp, js.ResponseReturnCode.CODE_200.value