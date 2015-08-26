import unittest

class ParametrizedTestCase(unittest.TestCase):
    # TestCase classes that want to be parametrized should inherit from this class.
    def __init__(self, methodName = 'runTest', param = None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcaseClass, param = None):
        # Create a suite containing all tests taken from the given subclass, passing them the parameter 'param'.
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcaseClass)
        print testnames
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcaseClass(name, param=param))
        return suite

class TestCase1(ParametrizedTestCase):
    def setUp(self):
        print "setUp"
        self.assertEqual(1, 1)

    def tearDown(self):
        print "tearDown"
        self.assertEqual(1, 1)

    def testRunTest(self):
        print 'param =', self.param
        self.assertEqual(1, 1)


def runAllTest():
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestCase1, [1, 2]))
    unittest.TextTestRunner(verbosity = 4).run(suite)
