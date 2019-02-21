import unittest

# import your test modules
import tests.test_login as test_login

loader = unittest.TestLoader()

suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_login))

runner = unittest.TextTestRunner(verbosity=3)

result = runner.run(suite)