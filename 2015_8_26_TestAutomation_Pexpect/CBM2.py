# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import threading,pexpect
from ssh import ssh
from log import log

class CBM2(threading.Thread):
    def __init__(self, cond, name,hostname,username,password,port=22):
        super(CBM2, self).__init__()
        self.cond = cond
        self.name = name
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
    def check_Billing_File(self):
        print "***Check file in query***                                        [4/5]"
        child = pexpect.spawn('telnet %s' % (self.hostname))
        log_checkConfiguration = log("Result_All_ListFile.log", 'w')
        child.logfile = log_checkConfiguration.logFile()
        index = child.expect(['login:', pexpect.EOF, pexpect.TIMEOUT], timeout=3)
        if index == 0:
            child.sendline(self.username)
            index = child.expect(['Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
            if index == 0:
                child.sendline(self.password)
                index = child.expect(['$', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                if index == 0:
                    child.sendline('su -')
                    index = child.expect(['Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                    if index == 0:
                        child.sendline('root')
                        index = child.expect(['#', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                        if index == 0:
                            child.sendline("billmtc")
                            index = child.expect(["BILLMTC", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                            if index == 0:
                                child.send("FILESYS\n\r")
                                index = child.expect(["18 Refresh", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                if index==0:
                                    child.send("LISTFILE AMA\n\r")
                                    index = child.expect(["RUNNING", pexpect.EOF, pexpect.TIMEOUT], timeout=15)
                                    if index==0:
                                        keylog_ListFile=log("Result_FILESYS_ListFile.log","w")
                                        flag=0
                                        while True:
                                            index=child.expect(["Size", pexpect.EOF, pexpect.TIMEOUT],timeout=5)
                                            if index==0:
                                                keylog_ListFile.keyLogAdd(child.before,child.after)
                                                flag=1
                                                continue

                                            elif index == 1:
                                                if flag==1:
                                                    pass
                                                else:
                                                    print "EOF when expect Size"
                                                break
                                            else:
                                                if flag==1:
                                                    pass
                                                else:
                                                    print "Timeout when expect Size"
                                                break
                                        print "\033[1;32;40m***Check file in query Success***                                [OK]\033[0m"

                                    elif index == 1:
                                        print "EOF when expect RUNNING"
                                    else:
                                        print "Timeout when expect RUNNING"

                                elif index == 1:
                                    print "EOF when expect 18 Refresh"
                                else:
                                    print "Timeout when expect 18 Refresh"

                            elif index == 1:
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
        self.cond.wait()
        self.check_Billing_File()#perform the action
        self.cond.release()
