# -*- coding:utf-8 -*-
import sys
from connect_send_expect import Session
import custom_exception as exception

class CBMCheckRTBConfiguration():
    def __init__(self, hostName, userName, password, rootUser, rootPasswd,timeout=5,traverseTimeout=1):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootUser = rootUser
        self.rootPasswd = rootPasswd
        self.timeout = timeout
        self.traverseTimeout = traverseTimeout

    def checkRTBConfiguration(self):
        try:
            print "***Checking Configuration***                                     [1/5]"
            session = Session(self.hostName, self.userName, self.password, self.rootUser, self.rootPasswd, "telnet", "checkRTBConfiguration.log")
            session.logfile = sys.stdout
            session.waitUntil(self.timeout, 'login:');        session.sendLine(self.userName)
            session.waitUntil(self.timeout, 'Password:');     session.sendLine(self.password)
            session.waitUntil(self.timeout, '$');             session.sendLine('su -')
            session.waitUntil(self.timeout, 'Password:');     session.sendLine(self.rootPasswd)
            session.waitUntil(self.timeout, '#');             session.sendLine('billmtc')
            session.waitUntil(self.timeout, 'BILLMTC')
            session.waitUntil(self.timeout, '18 Refresh');    session.send('schedule')
            session.waitUntil(self.timeout, 'schedule')
            session.waitUntil(self.timeout, '18 Refresh');    session.send('RTB')
            session.waitUntil(self.timeout, 'RTB')
            session.waitUntil(self.timeout, '18 Refresh');    session.send('Query AMA')
            session.waitUntil(self.timeout, '18 Refresh')
            session.waitUntil(self.timeout, '----------------------------------------------------')
            session.traverse("KeyLog_RTB.log",self.traverseTimeout,"INSV","SYSB","OFFL","ISTB")
            session.send('CONFRTB');        session.waitUntil(self.timeout, '18 Refresh')
            session.send('Query AMA');      session.waitUntil(self.timeout, '18 Refresh')
            session.waitUntil(self.timeout, '----------------------------------------------------')
            session.traverse("KeyLog_CONFRTB.log", self.traverseTimeout, "CONFIGURED","UNCONFIGURED" )
            session.send('')
            session.send('Quit');           session.waitUntil(self.timeout, '18 Refresh')
            session.send('Quit');           session.waitUntil(self.timeout, '18 Refresh')
            session.send('list');           session.waitUntil(self.timeout, 'Stream')

            flag=session.traverse2("KeyLog_SCHEDULE.log",self.traverseTimeout,"('Abort' quits)", "Continue")
            if flag==0:
                print "\033[1;32;40m***Checking configuration Success***                             [OK]\033[0m"
                return 0
            else:
                raise Exception.Fault_Error


        except exception.TimeOutError, e:
            print "Timeout"
            return 1

        except exception.EndOfFileError, e:
            print "EOF"
            return 2

        except exception.FaultError, e:
            print "Fault"
            return 3
