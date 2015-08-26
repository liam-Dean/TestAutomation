# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect,sys
from ssh import ssh
from log import log

class CBM1(threading.Thread):
    def __init__(self, cond, name,hostname,username,password,port=22):
        super(CBM1, self).__init__()
        self.cond = cond
        self.name = name
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
        self.ssh_connect=ssh(self.hostname,self.username,self.password,self.port)

    def check_config(self):
        print "***Checking Configuration***                                     [1/5]"
        child = pexpect.spawn('telnet %s' % (self.hostname))
        log_checkConfiguration=log("Result_All_CheckConfiguration.log",'w')
        child.logfile = log_checkConfiguration.logFile()
        index = child.expect(['login:',pexpect.EOF,pexpect.TIMEOUT],timeout=3)
        if index == 0:
            child.sendline(self.username)
            index = child.expect(['Password:',pexpect.EOF,pexpect.TIMEOUT],timeout=15)
            if index == 0:
                child.sendline(self.password)
                index = child.expect(['$',pexpect.EOF,pexpect.TIMEOUT],timeout=15)
                if index == 0:
                    child.sendline('su -')
                    index=child.expect(['Password:',pexpect.EOF,pexpect.TIMEOUT],timeout=15)
                    if index == 0:
                        child.sendline('root')
                        index=child.expect(['#',pexpect.EOF,pexpect.TIMEOUT],timeout=15)
                        if index == 0:
                            child.sendline("billmtc")
                            index=child.expect(["BILLMTC",pexpect.EOF,pexpect.TIMEOUT],timeout=15)
                            if index==0:
                                index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                if index ==0:
                                    child.before=''
                                    child.send('schedule\n\r')
                                    child.expect('schedule')
                                    index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                    if index == 0:
                                        child.send('RTB\n\r')
                                        child.expect('RTB')
                                        index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                        if index == 0:
                                            child.send('Query AMA\n\r')
                                            index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                            if index == 0:
                                                index = child.expect(["----------------------------------------------------", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
                                                if index == 0:
                                                    keyLog_RTB = log("Result_RTB_InSv.log",'w')
                                                    keyLog_RTB.keyLogWrite()
                                                    flag=0
                                                    while True:
                                                        index = child.expect(["INSV","SYSB","OFFL","ISTB", "MANB",pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                                        if index==0:
                                                            flag=1
                                                            print child.before
                                                            print child.after
                                                        elif index==1:
                                                            flag=1
                                                            print child.before
                                                            print child.after
                                                        elif index==2:
                                                            flag=1
                                                            print child.before
                                                            print child.after
                                                        elif index == 3:
                                                            flag=1
                                                            print child.before
                                                            print child.after
                                                        elif index == 4:
                                                            flag=1
                                                            print child.before
                                                            print child.after

                                                        elif index == 5:
                                                            if flag == 1:
                                                                pass
                                                            else:
                                                                print "EOF when expect INSV/SYSB/OFFL/ISTB/MANB"
                                                            break
                                                        else:
                                                            if flag == 1:
                                                                pass
                                                            else:
                                                                print "Timeout when expect INSV/SYSB/OFFL/ISTB/MANB"
                                                            break
                                                        keyLog_RTB.keyLogAdd(child.before,child.after)
                                                    child.send('CONFRTB\n\r')
                                                    index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)

                                                    if index==0:
                                                        child.send('Query AMA\n\r')
                                                        index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                                        if index == 0:
                                                            index = child.expect(["----------------------------------------------------", pexpect.EOF,pexpect.TIMEOUT], timeout=5)
                                                            if index == 0:
                                                                keyLog_ConfRTB=log("Result_CONFRTB_CONFIGURED.log", 'w')
                                                                keyLog_ConfRTB.keyLogWrite()
                                                                output = open("CONFRTB_result.log", "w")
                                                                flag=0
                                                                while True:
                                                                    index = child.expect(["CONFIGURED", "UNCONFIGURED", pexpect.EOF, pexpect.TIMEOUT],timeout=15)
                                                                    if index == 0:
                                                                        flag=1
                                                                        print child.before
                                                                        print child.after
                                                                    elif index == 1:
                                                                        flag=1
                                                                        print child.before
                                                                        print child.after

                                                                    elif index == 2:
                                                                        if flag == 1:
                                                                            pass
                                                                        else:
                                                                             print "EOF when expect CONFIGURED/UNCONFIGURED"
                                                                        break
                                                                    else:
                                                                        if flag == 1:
                                                                            pass
                                                                        else:
                                                                            print "Timeout when expect CONFIGURED/UNCONFIGURED"
                                                                        break

                                                                    keyLog_ConfRTB.keyLogAdd(child.before, child.after)

                                                                child.send('\n\r')
                                                                child.send('Quit\n\r')
                                                                index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT],timeout=15)
                                                                if index==0:
                                                                    child.send('Quit\n\r')
                                                                    index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                                                    if index==0:
                                                                        child.send('list\n\r')
                                                                        keyLog_SCHEDULE = log("Result_SCHEDULE_CONFIGURED.log", 'w')
                                                                        keyLog_SCHEDULE.keyLogWrite()
                                                                        flag=0
                                                                        index = child.expect(["Stream",pexpect.EOF, pexpect.TIMEOUT],timeout=5)
                                                                        keyLog_SCHEDULE.keyLogAdd(" ",child.after)
                                                                        if index == 0:
                                                                            while True:
                                                                                index = child.expect(["('Abort' quits)", "Continue",pexpect.EOF, pexpect.TIMEOUT],timeout=5)
                                                                                print child.before
                                                                                print child.after
                                                                                child.sendline('')
                                                                                keyLog_SCHEDULE.keyLogAdd(child.before,child.after)
                                                                                if index == 0:
                                                                                    flag = 1
                                                                                    continue
                                                                                elif index == 1:
                                                                                    flag=1
                                                                                    print "\033[1;32;40m***Checking configuration Success***                             [OK]\033[0m"
                                                                                    break
                                                                                elif index == 2:
                                                                                    if flag == 1:
                                                                                        pass
                                                                                    else:
                                                                                        print "EOF when expect SCHEDULE result"
                                                                                    break
                                                                                else:
                                                                                    if flag == 1:
                                                                                        pass
                                                                                    else:
                                                                                        print "Timeout when expect SCHEDULE result"
                                                                                    break

                                                                        elif index == 1:
                                                                            print "EOF when expect Stream"
                                                                        else:
                                                                            print "Timeout when expect Stream"

                                                                    elif index == 1:
                                                                        print "EOF when expect 18 Refresh"
                                                                    else:
                                                                        print "Timeout when expect 18 Refresh"

                                                                elif index == 1:
                                                                    print "EOF when expect 18 Refresh"
                                                                else:
                                                                    print "Timeout when expect 18 Refresh"

                                                            elif index == 1:
                                                                print "EOF when expect ----------------------------------------------------"
                                                            else:
                                                                print "Timeout when expect ----------------------------------------------------"

                                                        elif index == 1:
                                                            print "EOF when expect 18 Refresh"
                                                        else:
                                                            print "Timeout when expect 18 Refresh"

                                                    elif index == 1:
                                                        print "EOF when expect 18 Refresh"
                                                    else:
                                                        print "Timeout when expect 18 Refresh"

                                                elif index == 1:
                                                    print "EOF when expect ----------------------------------------------------"
                                                else:
                                                    print "Timeout when expect ----------------------------------------------------"

                                            elif index == 1:
                                                print "EOF when expect 18 Refresh"
                                            else:
                                                print "Timeout when expect 18 Refresh"

                                        elif index == 1:
                                            print "EOF when expect 18 Refresh"
                                        else:
                                            print "Timeout when expect 18 Refresh"

                                    elif index == 1:
                                        print "EOF when expect 18 Refresh"
                                    else:
                                        print "Timeout when expect 18 Refresh"

                                elif index == 1:
                                    print "EOF when expect 18 Refresh"
                                else:
                                    print "Timeout when expect 18 Refresh"

                            elif index==1:
                                print "EOF when expect BILLMTC"
                            else:
                                print "Timeout when expect BILLMTC"

                        elif index == 1:
                            print "EOF when expect #"
                        else:
                            print "Timeout when expect #"

                    elif index == 1:
                        print "EOF when expect Password"
                    else:
                        print "Timeout when expect Password"

                elif index == 1:
                    print "EOF when expect $"
                else:
                    print "Timeout when expect $"

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
        self.check_config()#perform the action
        self.cond.notify()
        self.cond.release()