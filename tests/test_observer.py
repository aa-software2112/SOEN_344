from tests.test_base import BaseTestClass
from uber_sante.models.availability import Availability
from uber_sante.models.scheduler import AppointmentRequestType
from uber_sante.miscellaneous.observer import *
from uber_sante.models.patient import *
from uber_sante.utils import cache


class ObserverTest(BaseTestClass):
	"""
	Assumes the server is running!
	"""

	def setUp(self):
		"""
		Must call setUp() on BaseTestClass to setup the test application
		"""

		super(ObserverTest, self).setUp()
		cache.reset_cache()



	def test_attach(self):
		""" testing all the cases of the attach method"""

		# case where the observable does not hold the patient_id

		observable = AvailabilityCanceledObservable()

		availability1 = Availability(2, 2, 32400, 53, 0, 2019, 3, 31, AppointmentRequestType.ANNUAL.value)

		patient_availability_pair = { 1 : availability1}

		observable.attach(patient_availability_pair)

		assert(observable.patient_id_availabilities.__contains__(1))
		assert(False, isinstance(observable.patient_id_availabilities[1], list))

		# now testing the case where the observable already holds the patient_id

		availability2 = Availability(3, 3, 32400, 103, 0, 2019, 3, 2, AppointmentRequestType.WALKIN.value)

		patient_availability_pair2 = {1: availability2}

		observable.attach(patient_availability_pair2)

		assert (isinstance(observable.patient_id_availabilities[1], list))

		# now testing that we append a availability to the list for the patient_id

		availability3 = Availability(4, 3, 3200, 100, 0 ,1990, 1,10,AppointmentRequestType.ANNUAL.value)

		patient_availability_pair3 = {1: availability3}

		observable.attach(patient_availability_pair3)

		assert(len(observable.patient_id_availabilities[1]) == 3)

	def test_notify(self):

		patient = Patient(1, "Samuel", "Gosselin", "bla", "2000", 'male', "21", "21", "222")
		set_to_cache(1, patient)

		observable = AvailabilityCanceledObservable()

		availability1 = Availability(2, 2, 32400, 53, 0, 2019, 3, 31, AppointmentRequestType.ANNUAL.value)

		patient_availability_pair = {1: availability1}

		observable.attach(patient_availability_pair)

		observable.notify()

		patient = get_from_cache(1)

		assert(len(patient.get_login_messages()) == 1)

	def test_detach(self):
		observable = AvailabilityCanceledObservable()

		availability1 = Availability(2, 2, 32400, 53, 0, 2019, 3, 31, AppointmentRequestType.ANNUAL.value)

		patient_availability_pair = {1: availability1}

		observable.attach(patient_availability_pair)

		observable.detach(1)

		assert(False, observable.patient_id_availabilities.__contains__(1))








