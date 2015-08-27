# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect
from ssh import ssh
from log import log


class Core(threading.Thread):
    def __init__(self, cond, name,hostname,username,password,port=22):
        super(Core, self).__init__()
        self.cond = cond
        self.name = name
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
    def call(self):
        child = pexpect.spawn('telnet %s' % (self.hostname))
        log_checkConfiguration = log("Result_All_Calling.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        index = child.expect(['>', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
        if index == 0:
            child.sendline(self.username + " " + self.password)
            index = child.expect(['CDMG S3MTXV19DN MS2K Sanity', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
            if index == 0:

                print "***Calling***                                                    [3/5]"
                child.sendline('mtxcrank cdr 10 10 10')
                index = child.expect('second')
                if index == 0:
                    print "\033[1;32;40m***Calling Success***                                            [OK]\033[0m"

                elif index == 1:
                    print "EOF when expect second"
                    print "***Error Occured when calling***"
                else:
                    print "Timeout when expect second"
                    print "***Error Occured when calling***"

                child.logfile.close()

            elif index == 1:
                print "EOF when expect CDMG S3MTXV19DN MS2K Sanity"
            else:
                print "Timeout when expect CDMG S3MTXV19DN MS2K Sanity"

        elif index == 1:
            print "EOF when expect login and password"
        else:
            print "Timeout when expect login and password"

    def run(self):
        self.cond.acquire()
        self.call()#perform the action
        self.cond.notify()
        self.cond.release()