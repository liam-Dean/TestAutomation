import pexpect, sys, custom_exception, ssh_connect, logger

class Session():
    def __init__(self, hostName, userName, password, rootName, rootPassword):
        super(Session, self).__init__()
        self.hostName = hostName
        self.userName = userName
        self.password = password
        self.rootName = rootName
        self.rootPassword = rootPassword

    def telnet(self):
        self.subSession = pexpect.spawn('telnet %s' % (self.hostName))
        return self.subSession

    def ssh(self):
        self.subSession = pexpect.spawn('ssh %s' % (self.hostName))
        return self.subSession

    def send(self, command):
        self.subSession.send(command + "\n\r")
        return 0

    def sendLine(self, command):
        session = self.subSession
        session.sendline(command)
        return 0

    def waitUntil(self, timeout = 5, Recv = " "):
        index = self.subSession.expect([pexpect.EOF, pexpect.TIMEOUT, Recv], timeout)
        if index == 0:
            raise custom_exception.EOF_Error
        elif index == 1:
            raise custom_exception.TimeOut_Error
        else:
            return 0 # 0 means Success

    def travelse(self, logDir = "", timeout = 1, *Recvs):
        flag = 0
        judge = [pexpect.EOF, pexpect.TIMEOUT]
        judge = judge + list(Recvs)

        if logDir == "":
            pass
        else:
            keyLog_RTB = logger.log(logDir, 'w')
            keyLog_RTB.keyLogWrite()
        while True:
            index = self.subSession.expect(judge, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.EOF_Error
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.TimeOut_Error
            else:
                flag = 1  # 1 means Success have one result
                print self.subSession.before + " " + self.subSession.after
                keyLog_RTB.keyLogAdd(self.subSession.before, self.subSession.after)
                continue

    def travelse2(self, logDir = "", timeout = 1, *Recvs):
        flag = 0
        judge = [pexpect.EOF, pexpect.TIMEOUT]
        judge = judge + list(Recvs)

        if logDir == "":
            pass
        else:
            keyLog = log.log(logDir, 'w')
            keyLog.keyLogWrite()
            keyLog.keyLogAdd(" ", self.subSession.after)
        while True:
            index = self.subSession.expect(judge, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.EOF_Error
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise custom_exception.TimeOut_Error
            else:
                flag = 1  # 1 means Success have one result
                print self.subSession.before + " " + self.subSession.after
                keyLog.keyLogAdd(self.subSession.before, self.subSession.after)
                continue
