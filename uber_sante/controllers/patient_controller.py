import os

from . import controllers
from uber_sante.utils import cookie_helper
from uber_sante.utils.date import Date
from uber_sante.models.patient import Patient
from uber_sante.services.patient_service import PatientService
from uber_sante.services.patient_service import CreatePatientStatus
from uber_sante.models.patient import MakeAnnualStatus
from uber_sante.services.availability_service import AvailabilityService
from uber_sante.models.scheduler import ScheduleRequest, Scheduler, RequestEnum, AppointmentRequestType
from uber_sante.utils import json_helper as js
from flask import Flask, request, jsonify, make_response
from uber_sante.utils.cache import get_from_cache, set_to_cache

patient_service = PatientService()
availability_service = AvailabilityService()


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


@controllers.route('/patient', methods=['GET', 'PUT'])
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


@controllers.route('/get_monthly_schedule', methods=['GET'])
def get_monthly_schedule():

    if request.method == 'GET':

        request_type = RequestEnum(request.args.get('request_type'))

        appointment_request_type = AppointmentRequestType(request.args.get('appointment_request_type'))

        year = int(request.args.get('year'))
        month = int(request.args.get('month'))

        sr_monthly = ScheduleRequest(request_type, appointment_request_type, Date(year, month))

        monthly_schedule = Scheduler.get_instance().get_schedule(sr_monthly)

        return js.create_json(monthly_schedule.as_dict(), None, js.ResponseReturnCode.CODE_200)


@controllers.route('/get_daily_schedule', methods=['GET'])
def get_daily_schedule():

    if request.method == 'GET':

        request_type = RequestEnum(request.args.get('request_type'))

        appointment_request_type = AppointmentRequestType(request.args.get('appointment_request_type'))

        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        day = int(request.args.get('day'))

        sr_daily = ScheduleRequest(request_type, appointment_request_type, Date(year, month, day))

        daily_schedule = Scheduler.get_instance().get_schedule(sr_daily)

        return js.create_json(daily_schedule.as_dict(), None, js.ResponseReturnCode.CODE_200)


@controllers.route('/make_annual_appointment', methods=['PUT'])
def make_annual_appointment():

    if request.method == 'PUT':

        availability_id = int(request.args.get('availability_id'))
        patient_id = request.args.get('patient_id')

        patient_service.test_and_set_patient_into_cache(patient_id)

        patient = get_from_cache(patient_id)

        availability = availability_service.get_availability(availability_id)


        result = patient.make_annual_appointment(availability)

        if result == MakeAnnualStatus.SUCCESS:
            return js.create_json(None, "Successfully added annual appointment", js.ResponseReturnCode.CODE_200)

        elif result == MakeAnnualStatus.HAS_ANNUAL_APPOINTMENT:
            return js.create_json(None, "Patient already has an annual appointment in cart",
                                  js.ResponseReturnCode.CODE_400)


@controllers.route('/make_walkin_appointment', methods=['PUT'])
def make_walkin_appointment():

    if request.method == 'PUT':

        availability_id = int(request.args.get('availability_id'))
        patient_id = request.args.get('patient_id')

        patient_service.test_and_set_patient_into_cache(patient_id)

        patient = get_from_cache(patient_id)

        availability = availability_service.get_availability(availability_id)

        patient.make_walkin_appointment(availability)

        return js.create_json(None, "Successfully added walkin appointment", js.ResponseReturnCode.CODE_200)

