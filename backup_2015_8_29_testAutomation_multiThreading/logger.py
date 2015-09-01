# -*- coding:utf-8 -*-
import os, os.path, time


class logger:
    def __init__(self, name, mode='w'):
        self.name = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())+" "+name
        self.mode = mode
        self.dir = os.getcwd()
        self.logDir = os.path.join(self.dir, "Log")
        self.logFileName = os.path.join(self.logDir, self.name)

        if os.path.exists(self.logDir):  # Make the path  if it doesn't exist
            pass
        else:
            os.mkdir(self.logDir)
        self.logFile()


    def logFile(self):
        self.logfile = open(self.logFileName, self.mode)
        return self.logfile

    def keyLogWrite(self, logDetail=" "):
        logfile = open(self.logFileName, 'w')
        logfile.write(logDetail)

    def keyLogAdd(self, before, after=None):
        logfile = open(self.logFileName, 'a')
        logfile.write(before)
        logfile.write(after)


if __name__ =='__main__':
    log=logger("case1.log")
    print time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())