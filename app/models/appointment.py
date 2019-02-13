class Appointment:
	"""Represents an appointment that goes into a patient's cart.
	When the appointment gets checked out it becomes a Booking object"""


	def __init__(self, availability_ids, date, patient_id, doctor_id, patient_name, doctor_name,
				  start_time, end_time):
		# by default an appointment is never considered booked
		self.booked = False

		# the availability_ids corresponds to primary key ids in the
		# availability table, they are used to validate and reserve the availabilities
		# and after are used as f_keys (foreign keys) for the booking object
		self.availability_ids = availability_ids

		# the date of the appointment
		self.date = date

		# the patient id and patient name 'might be' passed from cookie
		self.patient_id = patient_id
		self.patient_name = patient_name

		# doctor name and doctor id should be retrieved from the availability table, before creating this appointment obj
		self.doctor_name = doctor_name
		self.doctor_id = doctor_id

		# these may be passed from the availability objects
		self.start_time = start_time
		self.end_time = end_time







