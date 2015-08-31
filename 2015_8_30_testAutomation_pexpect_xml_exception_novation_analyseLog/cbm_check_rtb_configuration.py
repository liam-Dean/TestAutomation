# -*- coding:utf-8 -*-
import sys
from connect_send_expect import Session
import custom_exception as exception
import analyse_text

class CBMCheckRTBConfiguration():
    def __init__(self, hostName, userName, password, rootUser, rootPasswd, timeout = 5, traverseTimeout = 1,
                 stream = "AMA", fileFormat = "DIRP", destination = "defaultDestination", fileDestination = "/export/"):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootUser = rootUser
        self.rootPasswd = rootPasswd
        self.timeout = timeout
        self.traverseTimeout = traverseTimeout
        self.stream = stream
        self.fileFormat = fileFormat
        self.destination = destination
        self.fileDestination = fileDestination

    def checkRTBConfiguration(self):
        try:
            print "***Checking Configuration***                                     [1/5]"
            session = Session(self.hostName, self.userName, self.password, self.rootUser, self.rootPasswd, "telnet",
                              "checkRTBConfiguration.log")
            #session.logfile = sys.stdout
            session.waitUntil(self.timeout, 'login:')
            session.sendLine(self.userName)
            session.waitUntil(self.timeout, 'Password:')
            session.sendLine(self.password, 1)
            session.waitUntil(self.timeout, '$')
            session.sendLine('su -')
            session.waitUntil(self.timeout, 'Password:')
            session.sendLine(self.rootPasswd, 1)
            session.waitUntil(self.timeout, '#')
            session.sendLine('billmtc')
            session.waitUntil(self.timeout, 'BILLMTC')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('schedule')
            session.waitUntil(self.timeout, 'schedule')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('RTB')
            session.waitUntil(self.timeout, 'RTB')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('Query AMA')
            session.waitUntil(self.timeout, '18 Refresh')

            session.waitUntil(self.timeout, '----------------------------------------------------')
            flag, logFilePath = session.traverse("KeyLog_RTB.log", self.traverseTimeout, "stream", "INSV", "SYSB",
                                                 "OFFL", "ISTB", "MANB", )

            status = analyse_text.analyseRTBInSv(logFilePath, self.fileFormat, self.destination)

            session.send('CONFRTB')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('Query AMA')
            session.waitUntil(self.timeout, '18 Refresh')

            session.waitUntil(self.timeout, '----------------------------------------------------')

            flag, logFilePath = session.traverse("KeyLog_CONFRTB.log", self.traverseTimeout, "CONFIGURED", "CONFIGURED",
                                                 "UNCONFIGURED")

            configuration = analyse_text.analyseConfRTBConfigurated(logFilePath, self.fileFormat, self.destination)

            session.send('')
            session.send('Quit')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('Quit')
            session.waitUntil(self.timeout, '18 Refresh')
            session.send('list')
            session.waitUntil(self.timeout, 'Stream')


            flag, logFilePath = session.traverse2("KeyLog_SCHEDULE.log", self.traverseTimeout, "Return to Continue...",
                                                  "('Abort' quits)...", "Return to Continue...")
            verify = analyse_text.analyseScheduleInfo(logFilePath, self.stream, self.fileFormat, self.destination,
                                                      self.fileDestination)

            if status != "INSV":
                raise exception.RTBInSvError(self.stream, self.fileFormat, self.destination,status)
            if configuration != "CONFIGURED":
                raise exception.RTBConfigurationError(self.stream, self.fileFormat, self.destination,configuration)
            if verify != "success":
                raise exception.ScheduleError(self.stream, self.fileFormat, self.destination, self.fileDestination)

            print "\033[1;32;40m***Checking configuration Success***                             [OK]\033[0m"
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

        except exception.RTBInSvError, e:
            e.__RTBInSvError__()
            return 4

        except exception.RTBConfigurationError, e:
            e.__RTBConfigurationError__()
            return 5

        except exception.ScheduleError, e:
            e.__ScheduleError__()
            return 6
