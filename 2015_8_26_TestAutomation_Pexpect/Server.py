# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect
from ssh import ssh
from log import log


class Server(threading.Thread):
    def __init__(self, cond, name,hostname,username,password,port=22,fileDirection="./",action=0):
        super(Server, self).__init__()
        self.cond = cond
        self.name = name
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
        self.fileDirectory=fileDirection
        self.action=action

    def check_Billing_before_Transfer(self):
        child = pexpect.spawn('telnet %s' % (self.hostname))
        log_checkConfiguration = log("Result_All_CheckFileBeforeTransfer.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        print "***Got the billing before call***                                [2/5]"
        index = child.expect(['login:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
        if index == 0:
            child.sendline(self.username)
            index = child.expect(['Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
            if index == 0:
                child.sendline(self.password)
                index = child.expect(['cdma184%', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                if index == 0:
                    command = "cd " + self.fileDirectory + ";" + "ls -l" + '\n\r'
                    child.sendline(command)
                    index = child.expect(['cdma184%', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                    if index == 0:
                        print child.before
                        log_checkConfiguration.keyLogWrite(child.before)
                    elif index == 1:
                        print "EOF when expect cdma184%"
                    else:
                        print "Timeout when expect cdma184%"

                    child.logfile.close()
                    print "\033[1;32;40m***Got the billing before call Success***                        [OK]\033[0m"

                elif index == 1:
                    print "EOF when expect cdma184%"
                else:
                    print "Timeout when expect cdma184%"

            elif index == 1:
                print "EOF when expect Password"
            else:
                print "Timeout when expect Password"

        elif index == 1:
            print "EOF when expect login"
        else:
            print "Timeout when expect login"


    def check_Billing_after_Transfer(self):
        child = pexpect.spawn('telnet %s' % (self.hostname))
        log_checkConfiguration = log("Result_All_CheckFileAfterTransfer.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        print "***Got the billing after call***                                 [5/5]"
        index = child.expect(['login:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
        if index == 0:
            child.sendline(self.username)
            index = child.expect(['Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
            if index == 0:
                child.sendline(self.password)
                index = child.expect(['cdma184%', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                if index == 0:
                    command = "cd " + self.fileDirectory + ";" + "ls -l" + '\n\r'
                    child.sendline(command)
                    index = child.expect(['cdma184%', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                    if index == 0:
                        print child.before
                        log_checkConfiguration.keyLogWrite(child.before)
                    elif index == 1:
                        print "EOF when expect cdma184%"
                    else:
                        print "Timeout when expect cdma184%"

                    child.logfile.close()
                    print "\033[1;32;40m***Got the billing after call Success***                         [OK]\033[0m"

                elif index == 1:
                    print "EOF when expect cdma184%"
                else:
                    print "Timeout when expect cdma184%"

            elif index == 1:
                print "EOF when expect Password"
            else:
                print "Timeout when expect Password"

        elif index == 1:
            print "EOF when expect login"
        else:
            print "Timeout when expect login"

    def run(self):
        self.cond.acquire()
        if self.action==0:
            self.cond.wait()
            self.check_Billing_before_Transfer()#perform the action
            self.cond.notify()
            self.cond.release()
            return '2'
        else:
            self.check_Billing_after_Transfer()  # perform the action

