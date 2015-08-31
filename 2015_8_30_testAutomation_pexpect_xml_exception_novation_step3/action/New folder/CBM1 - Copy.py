# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect,sys,custom_exception
from ssh_connect import ssh
from logger import logger
from action import Session

class CBM1(threading.Thread):
    def __init__(self, cond, name,hostname,username,RootPasswd,password,port=22):
        super(CBM1, self).__init__()
        self.cond = cond
        self.name = name
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
        self.RootPasswd=RootPasswd
        self.ssh_connect=ssh(self.hostname,self.username,self.password,self.port)
        self.timeout=10
        self.traverseTimeout=1

    def check_config(self):
        print "***Checking Configuration***                                     [1/5]"
        session=Session()
        child=Session.telnet()
        log_checkConfiguration = log("Result_All_CheckConfiguration.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        try:
            Session.waitUntil('login:',self.timeout)
            Session.sendLine(self.username);    Session.waitUntil(self.timeout,'Password:')
            Session.sendLine(self.password);    Session.waitUntil(self.timeout,'$')
            Session.sendLine('su -');           Session.waitUntil(self.timeout,'Password:')
            Session.sendLine(self.RootPasswd);  Session.waitUntil(self.timeout,'#')
            Session.sendLine('billmtc');        Session.waitUntil(self.timeout,'BILLMTC');     Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('schedule');           Session.waitUntil(self.timeout,'schedule');    Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('RTB');                Session.waitUntil(self.timeout,'RTB');         Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('Query AMA');          Session.waitUntil(self.timeout,'18 Refresh');  Session.waitUntil(self.timeout,'----------------------------------------------------')

            Session.travelse("Result_RTB_InSv.log",self.traverseTimeout,"INSV","SYSB","OFFL","ISTB",)
            Session.send('CONFRTB');            Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('Query AMA');          Session.waitUntil(self.timeout,'18 Refresh'); Session.waitUntil(self.timeout, '----------------------------------------------------')

            Session.travelse("Result_CONFRTB_CONFIGURED.log",self.traverseTimeout,"CONFIGURED","UNCONFIGURED" )
            Session.send('')
            Session.send('Quit');               Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('Quit');               Session.waitUntil(self.timeout,'18 Refresh')
            Session.send('list');               Session.waitUntil(self.timeout,'Stream')

            flag=Session.travelse("Result_SCHEDULE_CONFIGURED.log",self.traverseTimeout,"('Abort' quits)", "Continue")

            if flag==0:
                print "\033[1;32;40m***Checking configuration Success***                             [OK]\033[0m"
            else:
                raise Exception.Fault_Error

        except  custom_exception.EOF_Error,e:
            print "EOF"

        except custom_exception.TimeOut_Error,e:
            print "Timeout"

        except custom_exception.Fault_Error,e:
            print "fault"
            

    def run(self):
        self.cond.acquire()
        self.check_config()#perform the action
        self.cond.notify()
        self.cond.release()