from uber_sante.services.patient_service import PatientService
from uber_sante.models.appointment import Appointment
from uber_sante.models.availability import Availability
from uber_sante.models.scheduler import AppointmentRequestType
from tests.test_base import BaseTestClass
from uber_sante.utils import cache
from uber_sante.utils.dbutil import DBUtil

class PatientTest(BaseTestClass):
    """
    Assumes the server is running!
    """

    def setUp(self):
        """
        Must call setUp() on BaseTestClass to setup the test application
        :return: N/A
        """
        super(PatientTest, self).setUp()
        self.patient_url = "http://localhost:5000/patient"
        self.patient_id = "16"
        self.availability_id = "20"
        cache.reset_cache()

        """ Log in user """
        self.login_url = "http://localhost:5000/login"
        self.valid_health_card_nb = "DRSJ 9971 0157"
        self.password = "password"
        valid_health_card_and_pw = {"health_card_nb": self.valid_health_card_nb,
                                    "password": self.password}

        response = self.send_post(self.login_url, valid_health_card_and_pw)
        self.assert_status_code(response, 200)

        """ Create and store patient in cache"""
        PatientService().test_and_set_patient_into_cache(self.patient_id)
        self.patient_1 = cache.get_from_cache(self.patient_id)
        self.availability_1 = Availability(self.availability_id, "20", "32400", "881", "1", "2019", "4", "8", AppointmentRequestType.WALKIN)
        self.appointment_1 = Appointment(self.patient_id, self.availability_1)


    def test_remove_appointment_endpoint_success(self):
        """
        Testing remove_appointment endpoint
        :return: N/A
        """
        self.patient_1.add_walkin_to_cart(self.appointment_1)

        valid_info = {"patient_id": self.patient_id, "availability_id":self.availability_id}

        response = self.send_delete(self.patient_url, valid_info)

        self.assert_status_code(response, 200)
        self.assert_json_message(response, "Appointment removed")

    def test_remove_appointment_endpoint_fail(self):
        """
        Testing remove_appointment endpoint
        :return: N/A
        """
        valid_info = {"patient_id": self.patient_id, "availability_id": self.availability_id}

        response = self.send_delete(self.patient_url, valid_info)

        self.assert_status_code(response, 400)
        self.assert_json_message(response, "Appointment not found/removed", error=True)

    def test_missing_remove_appointment_parameter(self):
        """
        Testing missing arguments for remove_appointment endpoint
        :return: N/A
        """
        patient_id_only = {"patient_id": self.patient_id}
        availability_id_only = {"availability_id": self.availability_id}

        response_patient = self.send_delete(self.patient_url, patient_id_only)
        response_availability = self.send_delete(self.patient_url, availability_id_only)

        self.assert_status_code(response_patient, 400)
        self.assert_json_message(response_patient, "No appointment specified", error=True)

        self.assert_status_code(response_availability, 400)
        self.assert_json_message(response_availability, "No patient specified", error=True)