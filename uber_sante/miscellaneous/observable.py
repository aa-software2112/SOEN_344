from abc import ABC, abstractmethod

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
		"""Detaches the observer from this Observable"""
		pass

	@abstractmethod
	def notify(self):
		"""Notifies the observers """
		pass


class AvailabilityCanceledObservable(Observable):

	def __init__(self):
		self.observers = set()

	def attach(self, observer_patient_id):
		pass

	def detach(self, observer):
		pass

	def notify(self):
		pass


if __name__ == "__main__":

	a = AvailabilityCanceledObservable()

	print(a.observers)

