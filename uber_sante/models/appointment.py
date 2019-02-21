from uber_sante.models.scheduler import AppointmentRequestType


class Appointment:
	"""Represents an appointment that goes into a patient's cart.
	When the appointment gets checked out it becomes a Booking object"""

	def __init__(self, patient_id, availability):

		# the patient id is passed from cookie
		self.patient_id = patient_id

		# the availability object corresponding to this appointment
		# has all the necessary information to display on the cart front end
		self.availability = availability

	def get_availability_id(self):
		return self.availability.id

	def is_walkin_appointment(self):
		if self.availability.get_type() == AppointmentRequestType.WALKIN:
			return True
		return False

	def is_annual_appointment(self):
		if self.availability.get_type() == AppointmentRequestType.ANNUAL:
			return True
		return False
