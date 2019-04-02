from flask import request
from flask import request

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js

from uber_sante.services.admin_service import AdminService
from uber_sante.services.nurse_service import CreateNurseStatus, NurseService
from uber_sante.services.doctor_service import DoctorService, CreateDoctorStatus
from uber_sante.models.medical_personel.medical_personel_runner import MedicalPersonelRunner

admin_service = AdminService()
doctor_service = DoctorService()
nurse_service = NurseService()

@controllers.route('/admin/register', methods=['PUT'])
def register_medical_personel():

    if request.method == 'PUT':

        # Check if logged in as admin
        if cookie_helper.user_is_logged(request, as_user_type=cookie_helper.UserTypes.ADMIN):
        
            request_object = request.get_json()




        else:
            return js.create_json(data=None, message="Not logged in as admin, cannot register medical personel",return_code=js.ResponseReturnCode.CODE_400)
            

@controllers.route('/admin/register/doctor', methods=['PUT'])
def register_doctor():

    if request.method == 'PUT':

        # Check if logged in as admin
        if cookie_helper.user_is_logged(request, as_user_type=cookie_helper.UserTypes.ADMIN):

            physician_permit_nb = request.get_json().get("physician_permit_nb")
            first_name = request.get_json().get("first_name")
            last_name = request.get_json().get("last_name")
            specialty = request.get_json().get("specialty")
            city = request.get_json().get("city")
            password = request.get_json().get("password")
            clinic_id = request.get_json().get("clinic_id")

            ret_val = doctor_service.create_doctor(
                physician_permit_nb,
                first_name,
                last_name,
                specialty,
                city,
                password,
                clinic_id
            )

            if ret_val == CreateDoctorStatus.PHYSICIAN_NUMBER_ALREADY_EXISTS:
                return js.create_json(data=None, message="Physician Number Already Exists", return_code=js.ResponseReturnCode.CODE_400)

            return js.create_json(data=None, message="Successfully created Doctor",return_code=js.ResponseReturnCode.CODE_201)

        else:
            return js.create_json(data=None, message="Not logged in as admin, cannot register a Doctor",return_code=js.ResponseReturnCode.CODE_400)

@controllers.route('/admin/register/nurse', methods=['PUT'])
def register_nurse():
    if request.method == 'PUT':

        # Check if logged in as admin
        if cookie_helper.user_is_logged(request, as_user_type=cookie_helper.UserTypes.ADMIN):

            access_id = request.get_json().get("access_id")
            first_name = request.get_json().get("first_name")
            last_name = request.get_json().get("last_name")
            password = request.get_json().get("password")
            clinic_id = request.get_json().get("clinic_id")

            ret_val = nurse_service.create_nurse(
                access_id,
                first_name,
                last_name,
                password,
                clinic_id
            )

            if ret_val == CreateNurseStatus.ACCESS_ID_ALREADY_EXISTS:
                return js.create_json(data=None, message="Access ID Already Exists", return_code=js.ResponseReturnCode.CODE_400)

            return js.create_json(data=None, message="Successfully created Nurse", return_code=js.ResponseReturnCode.CODE_201)

        else:
            return js.create_json(data=None, message="Not logged in as admin, cannot register a Nurse", return_code=js.ResponseReturnCode.CODE_400)

