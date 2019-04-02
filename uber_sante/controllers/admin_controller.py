from flask import request
from flask import request

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js

from uber_sante.services.admin_service import AdminService
from uber_sante.services.nurse_service import CreateNurseStatus, NurseService
from uber_sante.services.doctor_service import DoctorService, CreateDoctorStatus
from uber_sante.models.medical_personel.medical_personel_runner import MedicalPersonelRunner, MedicalPersonelStatus

admin_service = AdminService()
doctor_service = DoctorService()
nurse_service = NurseService()

@controllers.route('/admin/register', methods=['PUT'])
def register_medical_personel():

    if request.method == 'PUT':

        # Check if logged in as admin
        if cookie_helper.user_is_logged(request, as_user_type=cookie_helper.UserTypes.ADMIN):
        
            request_object = request.get_json()

            medical_personel_runner = MedicalPersonelRunner(request_object)
            result = medical_personel_runner.create_medical_personel()
            
            if result == MedicalPersonelStatus.MISSING_PARAMETERS:
                return js.create_json(data=None, message="Missing Parameters", return_code=js.ResponseReturnCode.CODE_400)

            if result == CreateDoctorStatus.PHYSICIAN_NUMBER_ALREADY_EXISTS:
                return js.create_json(data=None, message="Physician Number Already Exists", return_code=js.ResponseReturnCode.CODE_400)

            if result == CreateNurseStatus.ACCESS_ID_ALREADY_EXISTS:
                return js.create_json(data=None, message="Access ID Already Exists", return_code=js.ResponseReturnCode.CODE_400)

            return js.create_json(data=None, message="Successfully created Medical Personel",return_code=js.ResponseReturnCode.CODE_201)

        else:
            return js.create_json(data=None, message="Not logged in as admin, cannot register medical personel",return_code=js.ResponseReturnCode.CODE_400)
