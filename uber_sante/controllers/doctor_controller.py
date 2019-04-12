from uber_sante.services.clinic_service import ClinicService
from . import controllers
from flask import Flask, request, jsonify, make_response

from uber_sante.utils import cookie_helper
from uber_sante.utils.cookie_helper import *
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.models.scheduler import Scheduler

from uber_sante.services.doctor_service import DoctorService

doctor_service = DoctorService()
clinic_service = ClinicService()

@controllers.route('/doctor', methods=['GET', 'PUT', 'DELETE'])
def doctor():

    if request.method == 'GET':
        # params: id (int, semi-required), doctor_name (text, semi-required)
        # return: doctor object
        doctor_id = request.args.get('id')
        doctor_last_name = request.args.get('last_name')
        clinic_id = request.args.get('clinic_id')
        clinic_id_from_nurse = None

        if cookie_helper.user_is_logged(request, UserTypes.NURSE):
            clinic_list = clinic_service.get_current_clinic("nurse", int(request.cookies.get(CookieKeys.ID.value)))
            clinic_id_from_nurse = int(clinic_list[0]["id"])
          
        if doctor_id is None and doctor_last_name is None and clinic_id is None:
            return js.create_json(data=None, message='No doctor params specified', return_code=js.ResponseReturnCode.CODE_400)

        result = None

        if doctor_last_name is not None:
            result = doctor_service.get_doctor_by_last_name(doctor_last_name, clinic_id_from_nurse)
        elif clinic_id is not None:
            result = doctor_service.get_doctor_by_clinic(clinic_id)
        else:
            result = doctor_service.get_doctor(doctor_id)

        if result is None:
            return js.create_json(data=None, message='Could not retrieve doctor', return_code=js.ResponseReturnCode.CODE_500)
        if result == 3:
            return js.create_json(data=None, message='Doctor Id does not exist', return_code=js.ResponseReturnCode.CODE_400)
        if result == 4:
            return js.create_json(data=None, message=f"Doctor with last name '{doctor_last_name}' does not exist", return_code=js.ResponseReturnCode.CODE_400)
        
        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)
