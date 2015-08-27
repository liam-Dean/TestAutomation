import pexpect, custom_exception, logger, re

class Session():
    def __init__(self, hostName, userName, password, rootName, rootPassword, Protocal, logName):
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootName = rootName
        self.rootPassword = rootPassword
        if re.compile(Protocal, re.IGNORECASE).match("telnet"):
            self.telnetConnect()
        elif re.compile(Protocal, re.IGNORECASE).match("ssh"):
            self.sshConnect()
        else:
            self.telnetConnect()
        self.log=logger.Logger(logName,"w")

    def telnetConnect(self):
        self.subSession = pexpect.spawn('telnet %s' % (self.hostName))
        return self.subSession

    def sshConnect(self):
        self.subSession = pexpect.spawn('ssh %s' % (self.hostName))
        return self.subSession

    def send(self, command):
        self.subSession.send(command + "\n\r")
        self.log.logAdd("\n\r>> "+command+"\n\r")
        return 0    # 0 means success

    def sendLine(self, command):
        session = self.subSession
        session.sendline(command)
        self.log.logAdd("\n\r>> " + command+"\n\r")
        return 0    # 0 means success

    def waitUntil(self, timeout = 5, *receives):
        choiceList = [pexpect.EOF, pexpect.TIMEOUT]
        choiceList = choiceList + list(receives)
        index = self.subSession.expect(choiceList, timeout)
        if index == 0:
            raise custom_exception.EndOfFileError
        elif index == 1:
            raise custom_exception.TimeOutError
        else:
            self.log.logAdd("\n\r<< " + "\n\r")
            print self.subSession.before + " " + self.subSession.after
            self.log.logAdd(self.subSession.before+self.subSession.after)
            return 0 # 0 means Success

    def traverse(self, logName = "", timeout = 1, *receives):
        flag = 0
        choiceList = [pexpect.EOF, pexpect.TIMEOUT]
        choiceList = choiceList + list(receives)

        if logName == "":
            keyLog = logger.Logger("undefined_name.log", 'w')
        else:
            keyLog = logger.Logger(logName, 'w')
            keyLog.logWrite()
        while True:
            index = self.subSession.expect(choiceList, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.EndOfFileError
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.TimeOutError
            else:
                flag = 1  # 1 means Success have one result
                print self.subSession.before + " " + self.subSession.after
                keyLog.logAdd(self.subSession.before+self.subSession.after)
                self.log.logAdd("\n\r<< " + "\n\r")
                self.log.logAdd(self.subSession.before + self.subSession.after)
            continue

    def traverse2(self, logName = "", timeout = 1, *recvs):
        flag = 0
        choiceList = [pexpect.EOF, pexpect.TIMEOUT]
        choiceList = choiceList + list(recvs)

        if logName == "":
            keyLog = logger.Logger("undefined_name.log", 'w')
        else:
            keyLog = logger.Logger(logName, 'w')
            keyLog.logWrite()
            keyLog.logAdd(self.subSession.after)
        while True:
            index = self.subSession.expect(choiceList, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.EndOfFileError
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.TimeOutError
            else:
                flag = 1  # 1 means Success have one result
                print self.subSession.before + " " + self.subSession.after
                keyLog.logAdd(self.subSession.before+self.subSession.after)
                self.log.logAdd("\n\r<< " + "\n\r")
                self.log.logAdd(self.subSession.before + self.subSession.after)
                continue
