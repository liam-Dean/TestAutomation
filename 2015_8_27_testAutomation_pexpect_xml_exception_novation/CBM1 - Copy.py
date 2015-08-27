# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect,sys,Exception
from ssh import ssh
from log import log
from action import Channel

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
        CHANNEL=Channel()
        child=Channel.telnet()
        log_checkConfiguration = log("Result_All_CheckConfiguration.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        try:
            Channel.waitUntil('login:',self.timeout)
            Channel.sendLine(self.username);    Channel.waitUntil(self.timeout,'Password:')
            Channel.sendLine(self.password);    Channel.waitUntil(self.timeout,'$')
            Channel.sendLine('su -');           Channel.waitUntil(self.timeout,'Password:')
            Channel.sendLine(self.RootPasswd);  Channel.waitUntil(self.timeout,'#')
            Channel.sendLine('billmtc');        Channel.waitUntil(self.timeout,'BILLMTC');     Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('schedule');           Channel.waitUntil(self.timeout,'schedule');    Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('RTB');                Channel.waitUntil(self.timeout,'RTB');         Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('Query AMA');          Channel.waitUntil(self.timeout,'18 Refresh');  Channel.waitUntil(self.timeout,'----------------------------------------------------')

            Channel.travelse("Result_RTB_InSv.log",self.traverseTimeout,"INSV","SYSB","OFFL","ISTB",)
            Channel.send('CONFRTB');            Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('Query AMA');          Channel.waitUntil(self.timeout,'18 Refresh'); Channel.waitUntil(self.timeout, '----------------------------------------------------')

            Channel.travelse("Result_CONFRTB_CONFIGURED.log",self.traverseTimeout,"CONFIGURED","UNCONFIGURED" )
            Channel.send('')
            Channel.send('Quit');               Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('Quit');               Channel.waitUntil(self.timeout,'18 Refresh')
            Channel.send('list');               Channel.waitUntil(self.timeout,'Stream')

            flag=Channel.travelse("Result_SCHEDULE_CONFIGURED.log",self.traverseTimeout,"('Abort' quits)", "Continue")

            if flag==0:
                print "\033[1;32;40m***Checking configuration Success***                             [OK]\033[0m"
            else:
                raise Exception.Fault_Error

        except:
            pass

    def run(self):
        self.cond.acquire()
        self.check_config()#perform the action
        self.cond.notify()
        self.cond.release()