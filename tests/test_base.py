import unittest
from http.cookies import SimpleCookie
from uber_sante.utils import cookie_helper

from uber_sante import app

class BaseTestClass(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client(use_cookies=True)
        self.json_header = {'content-type': 'application/json'}
        self.valid_admin_email = "admin@ubersante.com"
        self.password = "admin"

    def send_post(self, url, dict_of_data=None):

        return self.custom_post(url, dict_of_data)

    def assert_json_data(self, response, expected):

        assert(response.json["data"] == expected)

    def assert_json_message(self, response, expected, error=False):

        if error:
            assert(response.json["error"]["message"] == expected)
        else:
            assert(response.json["message"] == expected)

    def assert_status_code(self, response, expected):
        assert(response.status_code == expected)

    def custom_post(self, url, dict_of_data=None, cookie={}):
        """
        A custom post implementation that allows injecting
        cookies into a request (to simulate a user with a cookie)
        :param url: the url to post to
        :param dict_of_data: the regular form data to send to the post
        :param cookie: the cookie of data (a dictionary of key:value pairs)
        :return: The response from the post
        """
        c = self.dict_to_cookie_string(cookie)

        return self.app.post(url, query_string=dict_of_data,
                             headers={'content-type': 'application/json',
                                      'COOKIE':c})
    def login_as_admin(self):

        valid_admin_login = {
            "email": self.valid_admin_email,
            "password": self.password
        }

        response = self.send_post(self.login_url, valid_admin_login)

        self.assert_status_code(response, 200)

    def dict_to_cookie_string(self, dict):

        c = []

        for k, v in dict.items():

            c.append(k + "=" + v + ";")

        return " ".join(c)