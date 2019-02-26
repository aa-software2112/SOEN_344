class Cart:
	def __init__(self):
		self.appointments = []

	def add_appointment(self, appointment):
		self.appointments.append(appointment)

	def get_appointment(self, availability_id):
		""" searches the list of appointment and returns the none that has the specified id"""
		for appointment in self.appointments:
			if appointment.get_availability_id() == availability_id:
				return appointment
		return None

	def remove_appointment(self, availability_id):
		""" searches through the list of appointments and if found it removes it and returns it"""
		index = 0

		for appointment in self.appointments:

			if appointment.get_availability_id() == availability_id:
				return self.appointments.pop(index)

			index = index + 1
		return None







