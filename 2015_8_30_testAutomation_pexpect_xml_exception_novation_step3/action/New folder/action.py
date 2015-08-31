__author__ = 'ezhicdi'
import threading,pexpect,sys,custom_exception,ssh_connect,logger
class Session():
    def __init__(self,hostname, username, RootPasswd, password, port=22):
        super(Session, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.RootPasswd = RootPasswd

    def telnet(self):
        self.child= pexpect.spawn('telnet %s' % (self.hostname))
        return self.child

    def ssh(self):
        self.child = pexpect.spawn('ssh %s' % (self.hostname))
        return self.child

    def sendLine(self,command):
        channel=self.child
        channel.sendline(command)
        return 0


    def send(self,command):
        self.child.send(command+"\n\r")
        return 0

    def waitUntil(self,timeout=5,Recv=" "):
        index = self.child.expect([ pexpect.EOF, pexpect.TIMEOUT,Recv], timeout)
        if index==0:
            raise Exception.EOF_Error
        elif index==1:
            raise Exception.TimeOut_Error
        else:
            return 0 #0 means Success

    def travelse(self, logDir="", timeout=1, *Recvs):
        flag = 0
        judge = [pexpect.EOF, pexpect.TIMEOUT]
        judge=judge+list(Recvs)

        if logDir == "":
            pass
        else:
            keyLog_RTB = log.log(logDir, 'w')
            keyLog_RTB.keyLogWrite()
        while True:
            index = self.child.expect(judge, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise Exception.EOF_Error
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise Exception.TimeOut_Error
            else:
                flag = 1  # 1 means Success have one result
                print self.child.before + " " + self.child.after
                keyLog_RTB.keyLogAdd(self.child.before, self.child.after)
                continue

    def travelse2(self, logDir="", timeout=1, *Recvs):
        flag = 0
        judge = [pexpect.EOF, pexpect.TIMEOUT]
        judge = judge + list(Recvs)

        if logDir == "":
            pass
        else:
            keyLog = log.log(logDir, 'w')
            keyLog.keyLogWrite()
            keyLog.keyLogAdd(" ", self.child.after)
        while True:
            index = self.child.expect(judge, timeout)
            if index == 0:
                if flag == 1:
                    return 0
                else:
                    raise Exception.EOF_Error
            elif index == 1:
                if flag == 1:
                    return 0
                else:
                    raise Exception.TimeOut_Error
            else:
                flag = 1  # 1 means Success have one result
                print self.child.before + " " + self.child.after
                keyLog.keyLogAdd(self.child.before, self.child.after)
                continue