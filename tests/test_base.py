import json
import unittest
from unittest.mock import MagicMock

from uber_sante import app
from uber_sante.utils.dbutil import DBUtil


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(use_cookies=True)
        self.json_header = {'content-type': 'application/json'}
        self.valid_admin_email = "admin@ubersante.com"
        self.password = "admin"
        self.write_fn = DBUtil.get_instance().write_one
        self.read_fn = DBUtil.get_instance().read_one

    def tearDown(self):
        DBUtil.get_instance().write_one = self.write_fn
        DBUtil.get_instance().read_one = self.read_fn

    def mock_db_read(self, return_value=None):
        DBUtil.get_instance().read_one = MagicMock(return_value=return_value)

    def mock_db_write(self, return_value=None):
        DBUtil.get_instance().write_one = MagicMock(return_value=return_value)

    def send_get(self, url, dict_of_data=None):

        return self.app.get(url, query_string=dict_of_data, headers=self.json_header)

    def send_post(self, url, dict_of_data=None):

        return self.custom_post(url, dict_of_data)

    def send_put(self, url, dict_of_data=None):

        return self.app.put(url, query_string=dict_of_data, headers=self.json_header)

    def send_delete(self, url, dict_of_data=None):

        return self.app.delete(url, query_string=dict_of_data, headers=self.json_header)

    def assert_json_data(self, response, expected):
        result = json.loads(response.get_data().decode("utf-8"))
        assert(result["data"] == expected)

    def assert_json_message(self, response, expected, error=False):
        result = json.loads(response.get_data().decode("utf-8"))
        if error:
            assert(result["error"]["message"] == expected)
        else:
            assert(result["message"] == expected)

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
                                      'COOKIE': c})

    def login_as_admin(self):

        valid_admin_login = {
            "email": self.valid_admin_email,
            "password": self.password
        }

        response = self.send_post("http://localhost:5000/login/admin", valid_admin_login)
        self.assert_status_code(response, 200)

    def dict_to_cookie_string(self, dict):

        c = []

        for k, v in dict.items():

            c.append(k + "=" + v + ";")

        return " ".join(c)
