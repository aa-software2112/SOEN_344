import unittest
import requests
import os

from uber_sante.tests.test_base import BaseTestClass
from uber_sante import app
from uber_sante.services.availability_service import AvailabilityService


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
        self.send_post(self.logout_url)

    def test_login_endpoint_success(self):
        valid_health_card_and_pw = {"health_card_nb": "XGCB 1090 0810",
                                    "password":"password"}

        response = self.send_post(self.login_url, valid_health_card_and_pw)

        assert(response.status_code == 200)
        assert(response.json["login_message"] == "Logged in successfully")

    def test_login_endpoint_fail(self):

        valid_health_card_invalid_pw = {"health_card_nb": "XGCB 1090 0810",
                                         "password": "invalidPassword"}

        invalid_health_card = {"health_card_nb": "XGCB 1090 081",
                                         "password": "password"}

        response = self.send_post(self.login_url,valid_health_card_invalid_pw)

        assert (response.status_code == 400)
        assert(response.json["login_message"] == "Invalid login information")

        response = self.send_post(self.login_url, invalid_health_card)

        assert (response.status_code == 400)
        assert (response.json["login_message"] == "Invalid login information")

