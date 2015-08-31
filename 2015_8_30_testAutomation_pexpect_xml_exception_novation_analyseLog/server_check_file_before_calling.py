# -*- coding:utf-8 -*-
from ssh_connect import SSH
from logger import Logger
from connect_send_expect import Session
import custom_exception as exception
import sys
import analyse_text

class ServerCheckFileBeforeCalling():
    def __init__(self, hostName, userName, password, rootUser, rootPasswd, fileDirection = "./", timeout = 5,
                 traverseTimeout = 1):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootUser = rootUser
        self.rootPasswd = rootPasswd
        self.timeout = timeout
        self.traverseTimeout = traverseTimeout
        self.fileDirectory = fileDirection

    def checkFile(self):
        session = Session(self.hostName, self.userName, self.password, self.rootUser, self.rootPasswd, "telnet",
                          "ServerCheckFileBeforeCalling.log")
        #session.logfile = sys.stdout
        print "***Got the billing before call***                                [2/5]"
        try:
            session.waitUntil(self.timeout, 'login:')
            session.sendLine(self.userName, 1)
            session.waitUntil(self.timeout, 'Password:')
            session.sendLine(self.password, 1)
            session.waitUntil(10, 'cdma184%')
            session.sendLine("cd " + self.fileDirectory + ";" + "ls -l" + "\n\r", 1)
            session.waitUntil(self.timeout, 'cdma184%')

            logPath = session.getLog()
            lastestNum = analyse_text.analyseBillingList(logPath)

            print "\033[1;32;40m***Got the billing before call Success***                        [OK]\033[0m"
            return 0, lastestNum

        except exception.TimeOutError, e:
            print "Timeout"
            return 1

        except exception.EndOfFileError, e:
            print "EOF"
            return 2

        except exception.FaultError, e:
            print "Fault"
            return 3
