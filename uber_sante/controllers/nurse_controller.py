from . import controllers
from flask import Flask, request, jsonify, make_response

from uber_sante.utils import json_helper as js
from uber_sante.utils import cookie_helper
from uber_sante.utils.cache import get_from_cache, set_to_cache
from uber_sante.models.patient import Patient, MakeAnnualStatus
from uber_sante.models.appointment import Appointment

from uber_sante.services.nurse_service import NurseService
from uber_sante.services.patient_service import PatientService
from uber_sante.services.availability_service import AvailabilityService
from uber_sante.services.booking_service import BookingService, BookingStatus

nurse_service = NurseService()
patient_service = PatientService()
availability_service = AvailabilityService()
booking_service = BookingService()

@controllers.route('/annual-appointment-nurse', methods=['PUT'])
def annual_appointment_nurse():

    if request.method == 'PUT':
        availability_id = int(request.get_json().get('availability_id'))
        patient_id = int(request.get_json().get('patient_id'))

        patient_service.test_and_set_patient_into_cache(patient_id)
        patient = get_from_cache(patient_id)
        availability = availability_service.get_availability(availability_id)
            
        result = booking_service.write_booking(Appointment(patient_id, availability))
        if result == BookingStatus.SUCCESS:
            return js.create_json(data=None, message="Successfully created annual booking", return_code=js.ResponseReturnCode.CODE_200)
        else:
            return js.create_json(data=None, message="Unable to create annual booking", return_code=js.ResponseReturnCode.CODE_400)



@controllers.route('/walkin-appointment-nurse', methods=['PUT'])
def walkin_appointment_nurse():

    if request.method == 'PUT':

        availability_id = int(request.get_json().get('availability_id'))
        patient_id = int(request.get_json().get('patient_id'))

        patient_service.test_and_set_patient_into_cache(patient_id)
        patient = get_from_cache(patient_id)
        availability = availability_service.get_availability(availability_id)

        result = booking_service.write_booking(Appointment(patient_id, availability))
        if result == BookingStatus.SUCCESS:
            return js.create_json(data=None, message="Successfully created walkin booking", return_code=js.ResponseReturnCode.CODE_200)
        else:
            return js.create_json(data=None, message="Unable to create walkin booking", return_code=js.ResponseReturnCode.CODE_400)
