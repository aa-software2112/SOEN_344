from flask import request, jsonify

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache

from uber_sante.services.clinic_service import ClinicService
from uber_sante.utils.time_interpreter import TimeInterpreter

clinic_service = ClinicService()
convert_time = TimeInterpreter()


@controllers.route('/clinic', methods=['GET', 'PUT', 'DELETE'])
def clinic():
    if request.method == 'GET':
        result = clinic_service.get_clinics()

        return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

    if request.method == 'PUT':

        if request.get_json() is None:
            return js.create_json(None, "No clinic information provided", js.ResponseReturnCode.CODE_400)

        name = request.get_json().get('name')
        location = request.get_json().get('location')
        nb_rooms = request.get_json().get('nb_rooms')
        nb_doctors = request.get_json().get('nb_doctors')
        nb_nurses = request.get_json().get('nb_nurses')
        open_time = convert_time.get_time_to_second(request.get_json().get('open_time'))
        close_time = convert_time.get_time_to_second(request.get_json().get('close_time'))
        phone = request.get_json().get('phone')
        clinic_id = request.get_json().get('clinic_id') #semi-required - indicated UPDATE

        if location is None:
            return js.create_json(data=None, message="No clinic location provided", return_code=js.ResponseReturnCode.CODE_400)
        if open_time is None:
            return js.create_json(data=None, message="No open time for clinic provided", return_code=js.ResponseReturnCode.CODE_400)
        if close_time is None:
            return js.create_json(data=None, message="No close time for clinic provided", return_code=js.ResponseReturnCode.CODE_400)
        if phone is None:
            return js.create_json(data=None, message="No phone number for clinic provided", return_code=js.ResponseReturnCode.CODE_400)
        
        #update clinic use case
        if clinic_id is not None:
            result = clinic_service.modify_clinic_limited(clinic_id, location, open_time, close_time, phone)
            
            if result is None:
                return js.create_json(data=None, message="Could not update clinic", return_code=js.ResponseReturnCode.CODE_500)

            return js.create_json(data=None, message="Successfully updated clinic", return_code=js.ResponseReturnCode.CODE_201)
        
        if name is None:
            return js.create_json(data=None, message="No clinic name provided", return_code=js.ResponseReturnCode.CODE_400)
        if nb_rooms is None:
            return js.create_json(data=None, message="Number of rooms for clinic not provided", return_code=js.ResponseReturnCode.CODE_400)
        if nb_doctors is None:
            return js.create_json(data=None, message="Number of doctors for clinic not provided", return_code=js.ResponseReturnCode.CODE_400)
        if nb_nurses is None:
            return js.create_json(data=None, message="Number of nurses for clininc not provided", return_code=js.ResponseReturnCode.CODE_400)

        result = clinic_service.register_clinic(name, location, nb_rooms, nb_doctors, nb_nurses, open_time, close_time, phone)

        if result is None:
            return js.create_json(data=None, message="Could not register clinic", return_code=js.ResponseReturnCode.CODE_500)

        return js.create_json(data=None, message="Successfully created clinic", return_code=js.ResponseReturnCode.CODE_201)


@controllers.route('/clinic/<string:user_type>/<string:id>', methods=['GET'])
def current_clinic(user_type, id):
    if request.method == 'GET':

        result = clinic_service.get_current_clinic(user_type, id)

        if result is not None:
            return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

        return js.create_json(data=None, message="Could not fetch current clinic.", return_code=js.ResponseReturnCode.CODE_400)
