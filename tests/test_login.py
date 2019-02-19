from uber_sante.services.patient_service import PatientService
from tests.test_base import BaseTestClass
from uber_sante.utils import cache


class LoginTest(BaseTestClass):
    """
    Assumes the server is running!
    """

    def setUp(self):
        """
        Must call setUp() on BaseTestClass to setup the test application

        :return: N/A
        """
        super(LoginTest, self).setUp()
        self.login_url = "http://localhost:5000/login"
        self.logout_url = "http://localhost:5000/logout"
        self.valid_health_card_nb = "XGCB 1090 0810"
        self.password = "password"
        self.send_post(self.logout_url)
        cache.reset_cache()

    def test_login_endpoint_success(self):
        """
        Testing login endpoint, and logged in successfully

        :return: N/A
        """
        valid_health_card_and_pw = {"health_card_nb": self.valid_health_card_nb,
                                    "password":self.password}

        response = self.send_post(self.login_url, valid_health_card_and_pw)

        assert(response.status_code == 200)
        assert(response.json["login_message"] == "Logged in successfully")

    def test_login_endpoint_fail(self):
        """
        Attempt login and expect login failure
        :return: N/A
        """
        valid_health_card_invalid_pw = {"health_card_nb": self.valid_health_card_nb,
                                         "password": "invalidPassword"}

        invalid_health_card = {"health_card_nb": "x",
                                         "password": self.password}

        response = self.send_post(self.login_url,valid_health_card_invalid_pw)

        assert (response.status_code == 400)
        assert (response.json["login_message"] == "Invalid login information")

        response = self.send_post(self.login_url, invalid_health_card)

        assert (response.status_code == 400)
        assert (response.json["login_message"] == "Invalid login information")

    def test_validate_login_info(self):
        """
        Make sure -1 is returned when login information is invalid, otherwise
        passes an actual ID

        :return: N/A
        """
        assert(PatientService().validate_login_info(self.valid_health_card_nb, self.password) > 0)
        assert(-1 == PatientService().validate_login_info(self.valid_health_card_nb, self.password + "INVALID"))

    def test_patient_in_cache_after_login(self):
        """
        Tests that the id returned from validate_login_info, when used to set the patient in cache,
        yields the correct patient object when retrieved from the cache

        :return: N/A
        """

        patient_id = PatientService().validate_login_info(self.valid_health_card_nb, self.password)

        assert(cache.get_from_cache(patient_id) == None)

        PatientService().test_and_set_patient_into_cache(patient_id)

        patient_obj = cache.get_from_cache(patient_id)

        assert(not (patient_obj == None))
        assert(patient_id == patient_obj.get_id())