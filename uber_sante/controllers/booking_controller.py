from flask import request, jsonify

from . import controllers

from uber_sante.utils import cookie_helper
from uber_sante.utils import json_helper as js
from uber_sante.utils.cache import get_from_cache

from uber_sante.models.scheduler import Scheduler
from uber_sante.models.appointment import Appointment

from uber_sante.services.booking_service import BookingService
from uber_sante.services.availability_service import AvailabilityService

booking_service = BookingService()
availability_service = AvailabilityService()

@controllers.route('/booking', methods=['GET', 'PUT', 'DELETE'])
def book():

    if request.method == 'GET':
        # example use case: get_bookings
        # params: patient_id (int, semi-required), doctor_id (int, semi-required)
        # return: booking(s) belonging to the patient or doctor
        # TODO: connect the call to the booking_service (line 28)

        patient_id = request.args.get('patient_id')
        doctor_id = request.args.get('doctor_id')

        if patient_id is None and doctor_id is None:
            return jsonify('No booking parameters specified'), 400

        results = True  # booking_service.get_booking(patient_id, doctor_id)

        return jsonify(results), 200


    if request.method == 'PUT':
        # example use case: checkout_appointment
        # params: appointment_id (int, required, from cookie), patient_id(int, required)
        # return: success/failure
        # TODO: implement patient cache to retrieve the appointment from the patient cache (line 48, 49)
        # TODO: connect the call to the scheduler class to try reserving the availability (line 51)
        # TODO: connect the call to the booking_service to create the booking in the Booking table (line 54)

        if not cookie_helper.user_is_logged(request):
            return js.create_json(data=None, message="User is not logged", return_code=js.ResponseReturnCode.CODE_400)

        availability_id = request.args.get('availability_id')
        patient_id = request.args.get('patient_id')
        booking_id = request.args.get('booking_id')

        if availability_id is None:
            return js.create_json(data=None, message="No appointment specified", return_code=js.ResponseReturnCode.CODE_400)
        if patient_id is None:
            return js.create_json(data=None, message="No patient specified", return_code=js.ResponseReturnCode.CODE_400)

        # update booking
        if booking_id is not None:
            availability_obj = availability_service.get_availability(availability_id)
            appointment = (Appointment(patient_id, availability_obj)) # creating appointment without using cart

            if availability_obj is not None:
                f_key = booking_service.cancel_booking_return_key(booking_id)

                if f_key:
                    Scheduler.get_instance().free_availability(f_key)
                    booking_service.write_booking(appointment)
                    return js.create_json(data={appointment}, message="Appointment successfully updated", return_code=js.ResponseReturnCode.CODE_200)
                else:
                    return js.create_json(data=None, message="Appointment not updated", return_code=js.ResponseReturnCode.CODE_400)
            else:
                return js.create_json(data=None, message="Unable to update booking", return_code=js.ResponseReturnCode.CODE_400)

        # TODO: Remove Dummy appointment below and use the implementation 
        patient = get_from_cache(patient_id)  # get the patient from cache
        appointment = patient.cart.get_appointment(availability_id)

        result = Scheduler.get_instance().reserve_appointment(appointment)

        if result:
            removed = patient.cart.remove_appointment(availability_id)
            booking_service.write_booking(appointment)
            
            if removed is None:
                return js.create_json(data=None, message="Appointment not found/removed", return_code=js.ResponseReturnCode.CODE_400)

            return js.create_json(data={appointment}, message="Appointment successfully booked", return_code=js.ResponseReturnCode.CODE_200)
        else:
            return js.create_json(data=None, message="Appointment slot already booked", return_code=js.ResponseReturnCode.CODE_400)


    if request.method == 'DELETE':
    # example use case: cancel_booking
    # params: booking_id (int, required)
    # return: success/failure

        booking_id = request.args.get('booking_id')
        
        if booking_id is None:
            return js.create_json(data=None, message="No booking specified", return_code=js.ResponseReturnCode.CODE_400)
        
        f_key = booking_service.cancel_booking_return_key(booking_id) # returns primary key of booking's corresponding availability
        if f_key:
            Scheduler.get_instance().free_availability(f_key)
        else:
            return js.create_json(data=None, message="Unable to delete booking", return_code=js.ResponseReturnCode.CODE_400)
        
        return js.create_json(data=None, message="Booking successfully deleted", return_code=js.ResponseReturnCode.CODE_200)

