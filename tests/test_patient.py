from tests.test_base import BaseTestClass

from uber_sante.utils import cache
from uber_sante.utils.dbutil import DBUtil

from uber_sante.models.appointment import Appointment
from uber_sante.models.availability import Availability
from uber_sante.models.scheduler import AppointmentRequestType

from uber_sante.services.patient_service import PatientService


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
        self.appointment_url = "http://localhost:5000/appointment"
        self.cart_url = "http://localhost:5000/cart"
        self.patient_id = "16"
        self.patient_id_fake = "-1"
        self.availability_id = "20"
        cache.reset_cache()

        """ Log in user """
        self.login_url = "http://localhost:5000/login"
        self.valid_health_card_nb = "DRSJ 9971 0157"
        self.password = "password"
        valid_health_card_and_pw = {
            "health_card_nb": self.valid_health_card_nb,
            "password": self.password
        }

        response = self.send_post(self.login_url, valid_health_card_and_pw)
        self.assert_status_code(response, 200)

        """ Create and store patient in cache"""
        PatientService().test_and_set_patient_into_cache(self.patient_id)
        self.patient_1 = cache.get_from_cache(self.patient_id)

        self.availability_1 = Availability(
            self.availability_id,
            "20",
            "32400",
            "881",
            "1",
            "2019",
            "4",
            "8",
            AppointmentRequestType.WALKIN)
        self.appointment_1 = Appointment(self.patient_id, self.availability_1)
        

    def test_remove_appointment_endpoint_success(self):
        """
        Testing remove_appointment endpoint
        :return: N/A
        """
        self.patient_1.add_walkin_to_cart(self.appointment_1)

        valid_info = {
            "patient_id": self.patient_id,
            "availability_id": self.availability_id
        }

        response = self.send_delete(self.appointment_url, valid_info)

        self.assert_status_code(response, 200)
        self.assert_json_message(response, "Appointment removed")


    def test_remove_appointment_endpoint_fail(self):
        """
        Testing remove_appointment endpoint
        :return: N/A
        """
        self.patient_1.add_walkin_to_cart(self.appointment_1)

        valid_info = {
            "patient_id": self.patient_id,
            "availability_id": self.availability_id
        }

        # Make sure the appointment is properly removed before testing the error.
        removed = self.send_delete(self.appointment_url, valid_info)
        self.assert_status_code(removed, 200)

        response = self.send_delete(self.appointment_url, valid_info)

        self.assert_status_code(response, 400)
        self.assert_json_message(response, "Appointment not found/removed", error=True)


    def test_missing_remove_appointment_parameter(self):
        """
        Testing missing arguments for remove_appointment endpoint
        :return: N/A
        """
        patient_id_only = {
            "patient_id": self.patient_id
        }
        availability_id_only = {
            "availability_id": self.availability_id
        }

        response_patient = self.send_delete(self.appointment_url, patient_id_only)
        response_availability = self.send_delete(self.appointment_url, availability_id_only)

        self.assert_status_code(response_patient, 400)
        self.assert_json_message(response_patient, "No appointment specified", error=True)

        self.assert_status_code(response_availability, 400)
        self.assert_json_message(response_availability, "No patient specified", error=True)


    def test_get_patient_by_id(self):
        """
        Test GET /patient with a valid Id
        :return: N/A
        """
        patient_id = {
            "patient_id": self.patient_id
        }
        response = self.send_get(self.patient_url, patient_id)
        self.assert_status_code(response, 200)
    

    def test_get_patient_no_id_provided(self):
        """
        Test GET /patient with no Id
        :return: N/A
        """
        response = self.send_get(self.patient_url)
        self.assert_status_code(response, 400)
        self.assert_json_message(response, "Patient Id is not specified", error=True)


    def test_get_patient_cannot_get(self):
        """
        Test GET /patient with a bad Id
        :return: N/A
        """
        patient_id_fake = {
            "patient_id": self.patient_id_fake
        }
        response = self.send_get(self.patient_url, patient_id_fake)
        self.assert_status_code(response, 500)
        self.assert_json_message(response, "Could not retrieve patient", error=True)

    
    # def test_put_patient(self):
    #     """
    #     Test PUT /patient with good object attributes
    #     :return: N/A
    #     """
    #     response = self.mock_db_write({
            # "health_card_nb": "AAAA 1111 1111",
            # "date_of_birth": "1900-01-01",
            # "gender": "M",
            # "phone_nb": "111-111-1111",
            # "home_address": "01 First Avenue",
            # "email": "johndoe@merriam-webster.com",
            # "first_name": "John",
            # "last_name": "Doe",
            # "password": "password123",
    #     })
    #     self.assert_status_code(response, 201)
    #     self.assert_json_message(response, "Patient record created", error=False)


    def test_put_patient_no_info(self):
        """
        Test PUT /patient with no object attributes
        :return: N/A
        """
        response = self.send_put(self.patient_url)
        self.assert_status_code(response, 400)
        self.assert_json_message(response, "No health card number provided", error=True)


    def test_put_patient_duplicate_health_card(self):
        """
        Test PUT /patient with duplicate health card number
        :return: N/A
        """
        patient_duplicate_health = {
            "health_card_nb": "XGCB 1090 0810",
            "date_of_birth": "1900-01-01",
            "gender": "M",
            "phone_nb": "111-111-1111",
            "home_address": "01 First Avenue",
            "email": "A",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
        }

        response = self.send_put(self.patient_url, patient_duplicate_health)
        self.assert_status_code(response, 500)
        self.assert_json_message(response, "Health card number already registered", error=True)

    
    def test_put_patient_duplicate_email(self):
        """
        Test PUT /patient with duplicate email
        :return: N/A
        """
        patient_duplicate_email = {
            "health_card_nb": "A",
            "date_of_birth": "1900-01-01",
            "gender": "M",
            "phone_nb": "111-111-1111",
            "home_address": "01 First Avenue",
            "email": "setridge0@ucsd.edu",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
        }
        
        response = self.send_put(self.patient_url, patient_duplicate_email)
        self.assert_status_code(response, 500)
        self.assert_json_message(response, "Email address already registered", error=True)

    def test_patient_view_cart(self):
        """
        Testing the view cart endpoint
        :return: N/A
        """

        self.patient_1.add_walkin_to_cart(self.appointment_1)

        response = self.send_get(self.cart_url)

        self.assert_status_code(response, 200)
        self.assert_json_message(response, "List of appointments with patient id")



