import unittest


from uber_sante import app

class BaseTestClass(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client(use_cookies=True)
        self.json_header = {'content-type': 'application/json'}

    def send_post(self, url, dict_of_data=None):

        return self.app.post(url, query_string=dict_of_data, headers=self.json_header)

    def send_delete(self, url, dict_of_data=None):

        return self.app.delete(url, query_string=dict_of_data, headers=self.json_header)

    def assert_json_data(self, response, expected):

        assert(response.json["data"] == expected)

    def assert_json_message(self, response, expected, error=False):

        if error:
            assert(response.json["error"]["message"] == expected)
        else:
            assert(response.json["message"] == expected)

    def assert_status_code(self, response, expected):
        assert(response.status_code == expected)