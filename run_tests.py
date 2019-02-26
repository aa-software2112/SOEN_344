import unittest

# import your test modules
import tests.test_login as test_login
import tests.test_patient as test_patient

loader = unittest.TestLoader()

suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_login))
suite.addTest(loader.loadTestsFromModule(test_patient))

runner = unittest.TextTestRunner(verbosity=3)

result = runner.run(suite)