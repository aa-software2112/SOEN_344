from flask import request, jsonify

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache

from uber_sante.services.clinic_service import ClinicService

clinic_service = ClinicService()


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
        open_time = request.get_json().get('open_time')
        close_time = request.get_json().get('close_time')

        if name is None:
            return js.create_json(data=None, message="No clinic name provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if location is None:
            return js.create_json(data=None, message="No clinic location provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if nb_rooms is None:
            return js.create_json(data=None, message="Number of rooms for clinic not provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if nb_doctors is None:
            return js.create_json(data=None, message="Number of doctors for clinic not provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if nb_nurses is None:
            return js.create_json(data=None, message="Number of nurses for clininc not provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if open_time is None:
            return js.create_json(data=None, message="No open time for clinic provided",
                                  return_code=js.ResponseReturnCode.CODE_400)
        if close_time is None:
            return js.create_json(data=None, message="No close time for clinic provided",
                                  return_code=js.ResponseReturnCode.CODE_400)

        result = clinic_service


@controllers.route('/clinic/<string:user_type>/<string:id>', methods=['GET'])
def current_clinic(user_type, id):
    if request.method == 'GET':

        result = clinic_service.get_current_clinic(user_type, id)

        if result is not None:
            return js.create_json(data=result, message=None, return_code=js.ResponseReturnCode.CODE_200)

        return js.create_json(data=None, message="Could not fetch current clinic.",
                              return_code=js.ResponseReturnCode.CODE_400)
