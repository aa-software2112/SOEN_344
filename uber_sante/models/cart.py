class Cart:
	def __init__(self):
		self.appointments = []

	def add_appointment(self, appointment):
		self.appointments.append(appointment)

	def remove_appointment(self, availability_id):
		""" searches through the list of appointments and if found it removes it and returns it"""
		for appointment in self.appointments:
			if appointment.get_availability_id() == availability_id:
				return self.appointments.pop(availability_id)
		return None







