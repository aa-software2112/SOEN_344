from datetime import *
from flask import Flask, request, jsonify, make_response

from . import controllers

from uber_sante.utils import cookie_helper, json_helper as js
from uber_sante.utils.date import Date
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.models.patient import Patient
from uber_sante.models.patient import MakeAnnualStatus
from uber_sante.models.scheduler import ScheduleRequest, Scheduler, RequestEnum, AppointmentRequestType

from uber_sante.services.patient_service import PatientService
from uber_sante.services.patient_service import CreatePatientStatus
from uber_sante.services.availability_service import AvailabilityService

from uber_sante.models.scheduler import ScheduleRequest, Scheduler, RequestEnum, AppointmentRequestType
from flask import Flask, request, jsonify, make_response
from uber_sante.utils.cookie_helper import *
from uber_sante.models.appointment import Appointment
from uber_sante.models.availability import Availability


patient_service = PatientService()
availability_service = AvailabilityService()


@controllers.route('/viewmycookie', methods=['GET'])
def view_cookie():

    return js.create_json(data=request.cookies, message="Here is your cookie", return_code=js.ResponseReturnCode.CODE_200)


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


@controllers.route('/login', methods=['POST', 'OPTIONS'])
def login():

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

        # set the cookie in the response object
        resp = js.create_json(data=None, message="Logged in successfully", return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, patient_id, cookie_helper.UserTypes.PATIENT.value)

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

        if request.get_json() is None:
            return js.create_json(None, "No patient information provided", js.ResponseReturnCode.CODE_400)

        health_card_nb = request.get_json().get('health_card_nb')
        date_of_birth = request.get_json().get('date_of_birth')
        gender = request.get_json().get('gender')
        phone_nb = request.get_json().get('phone_nb')
        home_address = request.get_json().get('home_address')
        email = request.get_json().get('email')
        first_name = request.get_json().get('first_name')
        last_name = request.get_json().get('last_name')
        password = request.get_json().get('password')

        if health_card_nb is None:
            return js.create_json(data=None, message="No health card number provided", return_code=js.ResponseReturnCode.CODE_400)
        if date_of_birth is None:
            return js.create_json(data=None, message="No data of birth provided", return_code=js.ResponseReturnCode.CODE_400)
        if gender is None:
            return js.create_json(data=None, message="No gender provided", return_code=js.ResponseReturnCode.CODE_400)
        if phone_nb is None:
            return js.create_json(data=None, message="No phone number provided", return_code=js.ResponseReturnCode.CODE_400)
        if home_address is None:
            return js.create_json(data=None, message="No home address provided", return_code=js.ResponseReturnCode.CODE_400)
        if email is None:
            return js.create_json(data=None, message="No email provided", return_code=js.ResponseReturnCode.CODE_400)
        if first_name is None:
            return js.create_json(data=None, message="No first name provided", return_code=js.ResponseReturnCode.CODE_400)
        if last_name is None:
            return js.create_json(data=None, message="No last name provided", return_code=js.ResponseReturnCode.CODE_400)
        if password is None:
            return js.create_json(data=None, message="No password provided", return_code=js.ResponseReturnCode.CODE_400)

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
            return js.create_json(data=None, message="Health card number already registered", return_code=js.ResponseReturnCode.CODE_500)

        if result == CreatePatientStatus.EMAIL_ALREADY_EXISTS:
            return js.create_json(data=None, message="Email address already registered", return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=None, message="Patient record created", return_code=js.ResponseReturnCode.CODE_201)

@controllers.route('/patient/<string:patient_id>', methods=['PUT'])
def update_patient(patient_id):

    if request.method == "PUT":
        # params: patient_id (string, required)
        # return: sucess/failure
        # note: the email and health card number of the user cannot be changed
        
        date_of_birth = request.args.get('date_of_birth')
        gender = request.args.get('gender')
        phone_nb = request.args.get('phone_nb')
        home_address = request.args.get('home_address')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        password = request.args.get('password')

        if patient_id is None:
            return js.create_json(data=None, message="No patient id provided", return_code=js.ResponseReturnCode.CODE_400)
        if date_of_birth is None:
            return js.create_json(data=None, message="No data of birth provided", return_code=js.ResponseReturnCode.CODE_400)
        if gender is None:
            return js.create_json(data=None, message="No gender provided", return_code=js.ResponseReturnCode.CODE_400)
        if phone_nb is None:
            return js.create_json(data=None, message="No phone number provided", return_code=js.ResponseReturnCode.CODE_400)
        if home_address is None:
            return js.create_json(data=None, message="No home address provided", return_code=js.ResponseReturnCode.CODE_400)
        if first_name is None:
            return js.create_json(data=None, message="No first name provided", return_code=js.ResponseReturnCode.CODE_400)
        if last_name is None:
            return js.create_json(data=None, message="No last name provided", return_code=js.ResponseReturnCode.CODE_400)
        if password is None:
            return js.create_json(data=None, message="No password provided", return_code=js.ResponseReturnCode.CODE_400)
         
        result = patient_service.update_patient(
            patient_id,
            date_of_birth,
            gender,
            phone_nb,
            home_address,
            first_name,
            last_name,
            password
        )

        if result == CreatePatientStatus.EMAIL_ALREADY_EXISTS:
            return js.create_json(data=None, message="Email address already registered", return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=None, message="Patient record updated", return_code=js.ResponseReturnCode.CODE_201)

@controllers.route('/get_schedule', methods=['POST'])
def get_schedule():

    if request.method == 'POST':

        request_type = RequestEnum(request.get_json().get('request_type'))
        appointment_request_type = AppointmentRequestType(request.get_json().get('appointment_request_type'))

        date = datetime.strptime(request.get_json().get('date'), '%Y-%m-%d').date()
        year = int(date.year)
        month = int(date.month)
        day = int(date.day)

        if request_type == RequestEnum.MONTHLY_REQUEST:
            sr_monthly = ScheduleRequest(request_type, appointment_request_type, Date(year, month))
            monthly_schedule = Scheduler.get_instance().get_schedule(sr_monthly)

            return js.create_json(data=monthly_schedule.as_dict(), message=None, return_code=js.ResponseReturnCode.CODE_200)

        if request_type == RequestEnum.DAILY_REQUEST:
            sr_daily = ScheduleRequest(request_type, appointment_request_type, Date(year, month, day))
            daily_schedule = Scheduler.get_instance().get_schedule(sr_daily)

            return js.create_json(data=daily_schedule.as_dict(), message=None, return_code=js.ResponseReturnCode.CODE_200)


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
            return js.create_json(data=None, message="Successfully added annual appointment", return_code=js.ResponseReturnCode.CODE_200)

        elif result == MakeAnnualStatus.HAS_ANNUAL_APPOINTMENT:
            return js.create_json(data=None, message="Patient already has an annual appointment in cart", return_code=js.ResponseReturnCode.CODE_400)


@controllers.route('/make_walkin_appointment', methods=['PUT'])
def make_walkin_appointment():

    if request.method == 'PUT':

        availability_id = int(request.args.get('availability_id'))
        patient_id = request.args.get('patient_id')

        patient_service.test_and_set_patient_into_cache(patient_id)
        patient = get_from_cache(patient_id)
        availability = availability_service.get_availability(availability_id)

        patient.make_walkin_appointment(availability)

        return js.create_json(data=None, message="Successfully added walkin appointment", return_code=js.ResponseReturnCode.CODE_200)


@controllers.route('/appointment', methods=['DELETE'])
def appointment():

    if request.method == 'DELETE':
        # example use case: remove appointment
        # params: patient_id (int, required), availability_id (int, required)
        # return: success/failure
        if not cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="User is not logged", return_code=js.ResponseReturnCode.CODE_400)

        patient_id = request.args.get('patient_id')
        availability_id = request.args.get('availability_id')

        if availability_id is None:
            return js.create_json(data=None, message="No appointment specified", return_code=js.ResponseReturnCode.CODE_400)
        if patient_id is None:
            return js.create_json(data=None, message="No patient specified", return_code=js.ResponseReturnCode.CODE_400)

        patient = get_from_cache(patient_id)
        result = patient.remove_from_cart(availability_id)

        if result is None:
            return js.create_json(data=None, message="Appointment not found/removed", return_code=js.ResponseReturnCode.CODE_400)

        return js.create_json(data=None, message="Appointment removed", return_code=js.ResponseReturnCode.CODE_200)

@controllers.route('/cart', methods=['GET'])
def cart():
    """ view cart use case """
    if request.method == 'GET':

        # ensure user is logged-in to proceed
        if not cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="User is not logged", return_code=js.ResponseReturnCode.CODE_400)

        # getting patient_id from cookie
        patient_id = request.cookies.get(CookieKeys.ID.value)
        # get patient from cache
        patient = get_from_cache(patient_id)

        cart = patient.get_cart()

        # list of Appointment objects
        appointment_list = cart.get_appointments()

        new_appointment_list = []

        # object parsing going on here to be able to send it with json format
        for appointment in appointment_list:
            new_availability = appointment.availability.__dict__
            new_appointment = Appointment(patient_id, new_availability).__dict__
            new_appointment_list.append(new_appointment)

        data_to_send = {'appointment_list': new_appointment_list, 'patient_id': patient_id}

        return js.create_json(data=data_to_send, message="List of appointments with patient id",
                              return_code=js.ResponseReturnCode.CODE_200)


