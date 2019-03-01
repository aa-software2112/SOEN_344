from flask import request

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js

from uber_sante.services.admin_service import AdminService
from uber_sante.services.doctor_service import DoctorService
from uber_sante.services.doctor_service import CreateDoctorStatus


admin_service = AdminService()
doctor_service = DoctorService()


@controllers.route('/loginAdmin', methods=['POST'])
def login_admin():
    """
    The endpoint for logging in as an administrator;
    This is necessary in order to register a doctor or a nurse -
    only an admin can do this
    """
    if request.method == 'POST':

        # User is already logged in (regardless of login-type {patient, admin, nurse, doctor})
        if cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="Already logged in",
                                  return_code=js.ResponseReturnCode.CODE_400)

        email = request.args.get('email')
        password = request.args.get('password')

        admin_id = admin_service.validate_login_info(email, password)

        if admin_id == -1:
            return js.create_json(data=None, message="Incorrect Admin Login information",
                                  return_code=js.ResponseReturnCode.CODE_400)

        resp = js.create_json(data=None, message="Logged in successfully",
                              return_code=js.ResponseReturnCode.CODE_200, as_tuple=False)
        resp = cookie_helper.set_user_logged(resp, admin_id,
                                             cookie_helper.UserTypes.ADMIN.value)

        return resp, js.ResponseReturnCode.CODE_200.value


@controllers.route('/registerDoctor', methods=['POST'])
def register_doctor():
    """
    Since the admin is responsible for registering a doctor, this method
    is put in the admin controller
    """

    if request.method == 'POST':

        # Check if logged in as admin
        if cookie_helper.user_is_logged(request, as_user_type=cookie_helper.UserTypes.ADMIN):

            physician_permit_nb = request.args.get("physician_permit_nb")
            first_name = request.args.get("first_name")
            last_name = request.args.get("last_name")
            specialty = request.args.get("specialty")
            city = request.args.get("city")
            password = request.args.get("password")

            ret_val = doctor_service.create_doctor(
                physician_permit_nb,
                first_name,
                last_name,
                specialty,
                city,
                password)

            if ret_val == CreateDoctorStatus.PHYSICIAN_NUMBER_ALREADY_EXISTS:
                return js.create_json(data=None, message="Physician Number Already Exists", return_code=js.ResponseReturnCode.CODE_400)

            return js.create_json(data=None, message="Successfully created doctor", return_code=js.ResponseReturnCode.CODE_200)

        else:
            return js.create_json(data=None, message="Not logged in as admin, cannot register a doctor", return_code=js.ResponseReturnCode.CODE_400)
