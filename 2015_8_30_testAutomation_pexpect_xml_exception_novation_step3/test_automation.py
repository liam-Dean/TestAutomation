# -*- coding:utf-8 -*-
from read_xml_config import ReadXMLConfig
from cbm_check_billing import CBMCheckBilling
from cbm_check_rtb_configuration import CBMCheckRTBConfiguration
from server_check_file_before_calling import ServerCheckFileBeforeCalling
from server_check_file_after_calling import ServerCheckFileAfterCalling
from core_calling import CoreCalling

if __name__ == '__main__':
    defaultTimeout = 3
    traverseTimeout = 1
    fileDirection = "/export/home/bsmbin/jasonDing/billing"  # define the direction of billing
    config = ReadXMLConfig('config_case1.xml').xmlGetTagAsDictionary()

    checkRTB            = CBMCheckRTBConfiguration(config["cluster_ip"], config["cluster_user"], config["cluster_password"], config["cluster_root_user"], config["cluster_root_password"], defaultTimeout, traverseTimeout)
    checkBeforeCalling  = ServerCheckFileBeforeCalling(config["server_ip"], config["server_user"], config["server_password"], config["server_user"], config["server_password"], fileDirection, defaultTimeout, traverseTimeout)
    calling             = CoreCalling(config["core_ip"], config["core_user"], config["core_password"],config["core_user"], config["core_password"], defaultTimeout, traverseTimeout)
    checkBilling        = CBMCheckBilling(config["cluster_ip"], config["cluster_user"], config["cluster_password"], config["cluster_root_user"], config["cluster_root_password"], defaultTimeout, traverseTimeout)
    checkAfterCalling   = ServerCheckFileAfterCalling(config["server_ip"], config["server_user"], config["server_password"], config["server_user"], config["server_password"], fileDirection, defaultTimeout, traverseTimeout)

    step1Result = checkRTB.checkRTBConfiguration()
    step2Result = checkBeforeCalling.checkFile()
    step3Result = calling.calling()
    step4Result = checkBilling.checkBilling()
    step5Result = checkAfterCalling.checkFile()
    print step1Result,step2Result,step3Result,step4Result,step5Result
    if step1Result|step2Result|step3Result|step4Result|step5Result == 0:
        print "\033[1;36;40m***Testing is success!***\033[0m"
    else:
        print "\033[1;31;40m***Some error occured ***\033[0m"