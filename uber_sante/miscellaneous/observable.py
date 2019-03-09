from abc import ABC, abstractmethod

# for my tests
from uber_sante.models.availability import Availability

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

	# 1. ready to test
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



		# in the code

		# get the booking_id on DELETE /booking
		# from the booking, get the patient and the availability_id
		pass

	def detach(self, patient_id):
		self.patient_id_availabilities.pop(patient_id)
		pass

	# 2
	def notify(self):
		# on /login, as soon as patient is set to cache notify all
		# because the patient that just logged-in and that is set to cache might be an observer
		# on the response login add the message to tell the user about the canceled booking

		pass


