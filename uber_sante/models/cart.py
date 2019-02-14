class Cart:
	def __init__(self):
		self.walk_ins = []
		self.annual = None

	def add_walk_in(self, walk_in):
		self.walk_ins.append(walk_in)

	def add_annual(self, annual):
		if self.annual is None:
			self.annual = annual

	def remove_walkin_appointment(self, availability_id):
		"""Removing the walk-in from the list and returning it"""
		for walk_in in self.walk_ins:
			if walk_in.get_availability_id() == availability_id:
				self.walk_ins.remove(walk_in)
				return walk_in


	def get_walkin_appts(self, availability_ids):
		"""Returns a list of walk-in appointments, or an empty list"""
		appts = []
		for availability_id in availability_ids:
			for walk_in in self.walk_ins:
				if walk_in.get_availability_id() == availability_id:
					appts.append(walk_in)
		return appts

	def get_annual_appt(self):
		return self.annual

	def remove_annual_appt(self):
		self.annual = None






