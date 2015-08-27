# -*- coding:utf-8 -*-
import base64, getpass, os, socket, sys, traceback, time, threading, os.path, logger, paramiko
from paramiko.py3compat import input
from read_xml_config import ReadXMLConfig
from CBM1 import CBM1
from CBM2 import CBM2
from Server import Server
from Core import Core

if __name__ == '__main__':
    fileDirection = "/export/home/bsmbin/jasonDing/billing"  # define the direction of billing
    condition1 = threading.Condition()  # define the lock of threading
    config = ReadXMLConfig('Config_Case1.xml').xmlGetTagAsDictionary()

    '''
        Check the Schedule configuration and check the file query before calling occured.
    '''
    cbm1 = CBM1(condition1, 'CBM1', config["cluster_ip"], config["cluster_user"], config["cluster_root_password"], config["cluster_password"], 22)  # create two thread within a condition lock
    server = Server(condition1, 'Server', config["server_ip"], config["server_user"], config["server_password"], 23, fileDirection, 0)
    server.start()  # server start first but the thread will set to wait when acquire the lock
    cbm1.start()  # Though start later but the thread will finish its processing first
    cbm1.join()
    server.join()  # Main thread wait until the thread above finish their tasks

    '''
        Calling happens with the command sent in Core.And then CBM will check the FIlESYS to findout whether the Billing is in the query
    '''

    cbm2 = CBM2(condition1, 'CBM2', config["cluster_ip"], config["cluster_user"], config["cluster_root_password"],config["cluster_password"], 22)  # create two thread within a condition lock
    core = Core(condition1, 'Core', config["core_ip"], config["core_user"], config["core_password"], 23)
    cbm2.start()  # cbm2 start first but the thread will set to wait when acquire the lock
    core.start()  # Though start later but the thread will finish its processing first
    core.join()
    cbm2.join()  # Main thread wait until the thread above finish their tasks

    '''
        After the process above , Server will double check the Destination of billing to confirm whether the transfering is success.
    '''

    # time.sleep() #suspend the Program for a while

    server = Server(condition1, 'Server', config["server_ip"], config["server_user"], config["server_password"], 23,fileDirection, 1)
    server.start()
    server.join()
    print "\033[1;34;40m***Testing is finished!***\033[0m"
