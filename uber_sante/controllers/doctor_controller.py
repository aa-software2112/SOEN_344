from . import controllers
from flask import Flask, request, jsonify, make_response

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.models.scheduler import Scheduler

from uber_sante.services.doctor_service import DoctorService

doctor_service = DoctorService()

@controllers.route('/doctor', methods=['GET', 'PUT', 'DELETE'])
def doctor():

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
