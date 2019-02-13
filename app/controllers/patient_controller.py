from . import controllers
from flask import request

class PatientController:
	def __init__(self, booking_controller):
		self.patients = []
		self.booking_controller = booking_controller

	def get_patient(self, patient_id):
		for patient in self.patients:
			if patient.get_id() == patient_id:
				return patient

	@controllers.route('/checkoutAppointment')
	def checkout_appointment(self):
		patient_id = request.args.get('patient_id')
		appointment_id = request.args.get('appointment_id')

		#TODO: see diagram 'Checkout Appointment Interaction Diagram'



