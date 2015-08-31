#!/usr/bin/env python
# -*- coding:utf-8 -*-

from read_xml_config import ReadXMLConfig
from cbm_check_billing import CBMCheckBilling
from cbm_check_rtb_configuration import CBMCheckRTBConfiguration
from server_check_file_before_calling import ServerCheckFileBeforeCalling
from server_check_file_after_calling import ServerCheckFileAfterCalling
from core_calling import CoreCalling
import analyse_text

if __name__ == '__main__':
    config = ReadXMLConfig('config_case1.xml').xmlGetTagAsDictionary() # Load the configuration
    config["defaultTimeout"] = int(config["defaultTimeout"])
    config["traverseTimeout"] = int(config["traverseTimeout"])

    checkRTB = CBMCheckRTBConfiguration(config["cluster_ip"], config["cluster_user"], config["cluster_password"],
                                        config["cluster_root_user"], config["cluster_root_password"],
                                        config["defaultTimeout"], config["traverseTimeout"], config["stream"],
                                        config["fileFormat"], config["destination"], config["fileDestination"])

    checkBeforeCalling = ServerCheckFileBeforeCalling(config["server_ip"], config["server_user"],
                                                      config["server_password"], config["server_user"],
                                                      config["server_password"], config["fileDestination"],
                                                      config["defaultTimeout"], config["traverseTimeout"])

    calling = CoreCalling(config["core_ip"], config["core_user"], config["core_password"], config["core_user"],
                          config["core_password"], config["defaultTimeout"], config["traverseTimeout"])

    checkBilling = CBMCheckBilling(config["cluster_ip"], config["cluster_user"], config["cluster_password"],
                                   config["cluster_root_user"], config["cluster_root_password"],
                                   config["defaultTimeout"], config["traverseTimeout"])

    checkAfterCalling = ServerCheckFileAfterCalling(config["server_ip"], config["server_user"],
                                                    config["server_password"], config["server_user"],
                                                    config["server_password"], config["fileDestination"],
                                                    config["defaultTimeout"], config["traverseTimeout"])

    step1Result = checkRTB.checkRTBConfiguration()
    step2Result, lastNum = checkBeforeCalling.checkFile()
    step3Result = calling.calling()
    step4Result = checkBilling.checkBilling()

    time.sleep


    step5Result, lastestNum = checkAfterCalling.checkFile()
    analyse_text.checkResult(step1Result, step2Result, step3Result, step4Result, step5Result)
