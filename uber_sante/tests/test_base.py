import os
import unittest

os.chdir("../../")
print(os.getcwd())

from uber_sante import app

class BaseTestClass(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client(use_cookies=True)
        self.json_header = {'content-type': 'application/json'}

    def send_post(self, url, dict_of_data=None):

        return self.app.post(url, query_string=dict_of_data, headers=self.json_header)