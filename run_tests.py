import unittest

# import your test modules
import tests.test_login as test_login
import tests.test_booking as test_booking

loader = unittest.TestLoader()

suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_login))
suite.addTest(loader.loadTestsFromModule(test_booking))


runner = unittest.TextTestRunner(verbosity=3)

result = runner.run(suite)