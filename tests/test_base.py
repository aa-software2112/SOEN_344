import unittest
from http.cookies import SimpleCookie
from uber_sante.utils import cookie_helper

from uber_sante import app

class BaseTestClass(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client(use_cookies=True)
        self.json_header = {'content-type': 'application/json'}
        self.admin_cookie = {cookie_helper.CookieKeys.LOGGED.value: "True",
                             cookie_helper.CookieKeys.ID.value: "1",
                             cookie_helper.CookieKeys.USER_TYPE.value: cookie_helper.UserTypes.ADMIN.value
        }

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

    def send_post_as_admin(self, url, dict_of_data=None):

        return self.custom_post(url, dict_of_data, self.admin_cookie)

    def dict_to_cookie_string(self, dict):

        c = []

        for k, v in dict.items():

            c.append(k + "=" + v + ";")

        return " ".join(c)