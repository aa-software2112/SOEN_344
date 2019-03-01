from unittest.mock import MagicMock

from tests.test_base import BaseTestClass

from uber_sante.utils import cache
from uber_sante.utils.dbutil import DBUtil

from uber_sante.services.admin_service import AdminService


class AdminTest(BaseTestClass):
    """
    Assumes the server is running!
    """

    def setUp(self):
        """
        Must call setUp() on BaseTestClass to setup the test application

        :return: N/A
        """
        super(AdminTest, self).setUp()
        self.login_url = "http://localhost:5000/loginAdmin"
        self.logout_url = "http://localhost:5000/logout"
        self.send_post(self.logout_url)
        cache.reset_cache()

        # For registering a doctor
        self.register_doctor_url = "http://localhost:5000/registerDoctor"
        self.doctor_information = {
            "physician_permit_nb": 1827364,
            "first_name": "Test",
            "last_name": "Doctor",
            "specialty": "TestDoctor",
            "city": "Montreal",
            "password": "sisyphus"
        }

    def test_admin_login_endpoint_success(self):
        """
        Testing login endpoint, and logged in successfully

        :return: N/A
        """
        valid_admin_login = {
            "email": self.valid_admin_email,
            "password": self.password
        }

        response = self.send_post(self.login_url, valid_admin_login)

        self.assert_status_code(response, 200)
        self.assert_json_message(response, "Logged in successfully")

    def test_admin_login_endpoint_fail(self):
        """
        Attempt login and expect login failure
        :return: N/A
        """
        valid_admin_login = {
            "email": self.valid_admin_email,
            "password": "invalidPassword"
        }

        invalid_admin_login = {
            "email": "invalid@email.com",
            "password": self.password
        }

        response = self.send_post(self.login_url, valid_admin_login)

        self.assert_status_code(response, 400)
        self.assert_json_message(response, "Incorrect Admin Login information", error=True)

        response = self.send_post(self.login_url, invalid_admin_login)

        self.assert_status_code(response, 400)
        self.assert_json_message(response, "Incorrect Admin Login information", error=True)

    def test_admin_service_validate_login_info(self):
        """
        Make sure -1 is returned when login information is invalid, otherwise
        passes an actual ID

        :return: N/A
        """
        assert(AdminService().validate_login_info(self.valid_admin_email, self.password) > 0)
        assert(-1 == AdminService().validate_login_info(self.valid_admin_email, self.password + "INVALID"))

    def test_register_doctor(self):
        """
        Create a doctor, and verify that it was created successfully

        :return: N/A
        """
        self.login_as_admin()

        self.mock_db_read()
        self.mock_db_write()

        resp = self.send_post(self.register_doctor_url, self.doctor_information)
        self.assert_status_code(resp, 200)
