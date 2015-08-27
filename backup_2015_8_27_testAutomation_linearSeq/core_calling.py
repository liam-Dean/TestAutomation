# -*- coding:utf-8 -*-
import sys
from connect_send_expect import Session
import custom_exception as exception

class CoreCalling():
    def __init__(self, hostName, userName, password, rootUser, rootPasswd, timeout = 5, traverseTimeout = 1):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootUser = rootUser
        self.rootPasswd = rootPasswd
        self.timeout = timeout
        self.traverseTimeout = traverseTimeout

    def calling(self):
        session = Session(self.hostName, self.userName, self.password, self.rootUser, self.rootPasswd, "telnet", "CoreCalling.log")
        session.logfile = sys.stdout
        print "***Calling***                                                    [3/5]"
        try:
            session.waitUntil(self.timeout, '>')
            session.sendLine(self.userName + " " + self.password)
            session.waitUntil(self.timeout, 'CDMG S3MTXV19DN MS2K Sanity')
            session.sendLine('mtxcrank cdr 10 10 10')
            session.waitUntil(self.timeout, 'second')
            print "\033[1;32;40m***Calling Success***                                            [OK]\033[0m"
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
