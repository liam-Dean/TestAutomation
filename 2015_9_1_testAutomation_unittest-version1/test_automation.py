#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import unittest
from read_xml_config import ReadXMLConfig
from check_configuration import CheckConfiguration
from check_file import CheckFile
from generate_call import GenerateCall

# testClass
class testCase1(unittest.TestCase):
    def setUp(self):
        config = ReadXMLConfig('config_case1.xml').xmlGetTagAsDictionary()    # Load the configuration
        self.checkConfiguration = CheckConfiguration(config["cluster_ip"], config["cluster_user"],
                                                     config["cluster_password"], config["cluster_root_user"],
                                                     config["cluster_root_password"], int(config["defaultTimeout"]),
                                                     int(config["traverseTimeout"]), config["stream"],
                                                     config["fileFormat"], config["destination"],
                                                     config["fileDestination"])

        self.checkFile = CheckFile(config["server_ip"], config["server_user"], config["server_password"],
                                   config["server_user"], config["server_password"], config["fileDestination"],
                                   int(config["defaultTimeout"]), int(config["traverseTimeout"]))

        self.generateCall = GenerateCall(config["core_ip"], config["core_user"], config["core_password"],
                                         config["core_user"], config["core_password"], int(config["defaultTimeout"]),
                                         int(config["traverseTimeout"]))

        self.assertEqual(self.checkConfiguration.isExist(), True)

    def tearDown(self):
        # rewind the configuration
        pass

    def testCase1(self):
        self.assertIsInstance(self.checkFile.lastFileNumber(), long)
        self.assertEqual(self.generateCall.isSuccess(), True)
        self.assertIsInstance(self.checkFile.lastFileNumber(), long)

# pre-built test suite
def buildTestSuite():
    suite = unittest.TestSuite()
    testSuiteMap = ['testCase1']
    return unittest.TestSuite(map(testCase1, testSuiteMap))

# runTest
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    testSuite = buildTestSuite()
    runner.run(testSuite)
