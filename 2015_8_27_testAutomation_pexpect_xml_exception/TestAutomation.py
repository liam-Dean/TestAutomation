# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'
import base64 , getpass , os , socket , sys , traceback,time,threading,pexpect,os.path,log,paramiko,interactive
from paramiko.py3compat import input
import read_Config
from CBM1 import CBM1
from CBM2 import CBM2
from Server import Server
from Core import Core



if __name__== '__main__':
    '''
        Define the Variants
    '''
    UseGSSAPI = True             # enable GSS-API / SSPI authentication
    DoGSSAPIKeyExchange = True
    curr_prompt=">>"
    curr_ssh = None
    username   = ''
    hostname   = ''
    password   = ''
    hostpath = ''
    localpath  = ''
    default_hostname = ''
    default_username = ''
    fileDirection="/export/home/bsmbin/jasonDing/billing"

    CBM = {"hostname": "",
           "username": "",
           "password": "",
           "port": 23,
           "protocal": "",
           "RootPassword":""
           }

    SERVER = {"hostname": "",
             "username": "",
             "password": "",
             "port": 23,
             "protocal": ""
             }

    CORE = {"hostname": "",
            "username": "",
            "password": "",
            "port": 23,
            "protocal": ""
            }

    CBM, CORE, SERVER = read_Config.read_Config(CBM, CORE, SERVER)

    condition1=threading.Condition()
    condition2=threading.Condition()
    condition3=threading.Condition()
    '''
        Check the Schedule configuration and check the file query before calling occured.
    '''
    cbm1    = CBM1(condition1, 'CBM1',CBM["hostname"],CBM["username"],CBM["RootPassword"],CBM["password"],CBM["port"])      #create two thread within a condition lock
    server  = Server(condition1,'Server',"202.38.35.184","bsmbin","Abcde01!",23,fileDirection,0)
    server.start()  #server start first but the thread will set to wait when acquire the lock
    cbm1.start()    #Though start later but the thread will finish its processing first
    cbm1.join()
    server.join()   #Main thread wait until the thread above finish their tasks

    '''
        Calling happens with the command sent in Core.And then CBM will check the FIlESYS to findout whether the Billing is in the query
    '''

    cbm2 = CBM2(condition2, 'CBM2',"10.178.28.26","nortel","nortel",22)         #create two thread within a condition lock
    core = Core(condition2,'Core',"10.24.16.134","lisa","lisa",23)
    cbm2.start()     #cbm2 start first but the thread will set to wait when acquire the lock
    core.start()     #Though start later but the thread will finish its processing first
    core.join()
    cbm2.join()      #Main thread wait until the thread above finish their tasks

    '''
        After the process above , Server will double check the Destination of billing to confirm whether the transfering is success.
    '''

    #time.sleep() #suspend the Program for a while

    server  = Server(condition3,'Server',"202.38.35.184","bsmbin","Abcde01!",23,fileDirection,1)
    server.start()
    server.join()
    print "\033[1;34;40m***Testing is finished!***\033[0m"

