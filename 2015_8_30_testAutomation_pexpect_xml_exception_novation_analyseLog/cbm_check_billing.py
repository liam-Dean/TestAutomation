# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import sys
from connect_send_expect import Session
import custom_exception as exception

class CBMCheckBilling():
    def __init__(self, hostName, userName, password, rootUser, rootPasswd,timeout=5,traverseTimeout=1):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootUser = rootUser
        self.rootPasswd = rootPasswd
        self.timeout = timeout
        self.traverseTimeout = traverseTimeout

    def checkBilling(self):
        print "***Check file in query***                                        [4/5]"
        try:
            session = Session(self.hostName, self.userName, self.password, self.rootUser, self.rootPasswd, "telnet","checkBilling.log")
            #session.logfile = sys.stdout
            session.waitUntil(self.timeout, 'login:')
            session.sendLine(self.userName,1)
            session.waitUntil(self.timeout, 'Password:')
            session.sendLine(self.password,1)
            session.waitUntil(self.timeout, '$')
            session.sendLine('su -')
            session.waitUntil(self.timeout, 'Password:')
            session.sendLine(self.rootPasswd,1)
            session.waitUntil(self.timeout, '#')
            session.sendLine('billmtc')
            session.waitUntil(self.timeout, 'BILLMTC')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('FILESYS')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('LISTFILE AMA')
            session.waitUntil(self.timeout, 'RUNNING')
            session.waitUntil(self.timeout, 'O')
            print "\033[1;32;40m***Check file in query Success***                                [OK]\033[0m"
            return 0

        except exception.TimeOutError, e:
                print "Timeout"
                return 1

        except exception.EndOfFileError, e:
            print "EOF"
            return 2

        except exception.FaultError, e:
            print "Fault"
            return 3
