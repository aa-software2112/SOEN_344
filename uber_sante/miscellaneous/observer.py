from abc import ABC, abstractmethod

from uber_sante.utils.cache import *


class Observable(ABC):
	"""
		The abstract class that defines the methods for the
		Observer design pattern
	"""

	@abstractmethod
	def attach(self, observer):
		"""Attaches an observer to this Observable"""
		pass

	@abstractmethod
	def detach(self, observer):
		"""Detaches an observer from this Observable"""
		pass

	@abstractmethod
	def notify(self):
		"""Notifies the observer(s) """
		pass


class AvailabilityCanceledObservable(Observable):
	""" Act as a patient notifier on login"""

	def __init__(self):
		# dict, 'keys' are patient_id mapping to availability objects
		# corresponding to the canceled booking
		self.patient_id_availabilities = {}

	def attach(self, patient_id_availability_pair):
		"""
		Attaches a patient_id_availability_pair to this notifier
		:param patient_id_availability_pair: { 'patient_id' : availability_obj }
		:return: void
		"""

		# getting the patient id from the dictionary
		key = next(iter(patient_id_availability_pair))

		# verifying if the patient is already set to be notified
		# of a canceled booking
		if self.patient_id_availabilities.__contains__(key):
			if isinstance(self.patient_id_availabilities[key], list):
				self.patient_id_availabilities[key].append(patient_id_availability_pair[key])
			else:
				# the key has only one value so we create a list of the now 2 values
				availability_list = [self.patient_id_availabilities[key], patient_id_availability_pair[key]]
				# put the list back in the dict
				self.patient_id_availabilities[key] = availability_list
		else:
			self.patient_id_availabilities.update(patient_id_availability_pair)

	def detach(self, patient_id):
		self.patient_id_availabilities.pop(patient_id)

	def notify(self):
		# when a patient logs in, we verify if he is within the group of
		# patients that we need to notify
		for patient_id in self.patient_id_availabilities:
			if patient_id in cache:
				# then the user just logged in
				patient = get_from_cache(patient_id)
				patient.update(self.patient_id_availabilities[patient_id])
				# we can now detach the patient
				self.detach(patient_id)

notifier = AvailabilityCanceledObservable()

if __name__ == '__main__':
	print("problem fixed :)")