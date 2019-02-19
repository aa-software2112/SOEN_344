class Appointment:
	"""Represents an appointment that goes into a patient's cart.
	When the appointment gets checked out it becomes a Booking object"""


	def __init__(self, patient_id, patient_name, availability, booking_type):

		# the patient id and name are passed from cookie
		self.patient_id = patient_id
		self.patient_name = patient_name

		# the availability object corresponding to this appointment
		# has all the necessary information to display on the cart front end
		self.availability = availability

		# annual or walkin
		self.type = booking_type

	def get_availability_id(self):
		return self.availability.id








