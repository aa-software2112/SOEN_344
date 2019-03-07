import unittest

# import your test modules
import tests.test_login as test_login
import tests.test_admin as test_admin
import tests.test_patient as test_patient
import tests.test_booking as test_booking
import tests.test_availability as test_availability

loader = unittest.TestLoader()

suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_login))
suite.addTest(loader.loadTestsFromModule(test_admin))
suite.addTest(loader.loadTestsFromModule(test_booking))
suite.addTest(loader.loadTestsFromModule(test_patient))
suite.addTest(loader.loadTestsFromModule(test_availability))

runner = unittest.TextTestRunner(verbosity=3)

result = runner.run(suite)