# -*- coding:utf-8 -*-
import os, os.path, time

class Logger:
    def __init__(self, name, mode = 'a+'):
        self.name = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()) + "_" + name
        self.mode = mode
        self.dir = os.getcwd()
        self.logDir = os.path.join(self.dir, "Log")

        if os.path.exists(self.logDir):  # Make the path  if it doesn't exist
            pass
        else:
            os.mkdir(self.logDir)

        self.logFileName = os.path.join(self.logDir, self.name)
        self.logFile()

    def logFile(self):
        self.logfile = open(self.logFileName, self.mode)
        return self.logfile

    def logWrite(self, writeLogDetail = " "):
        logfile = open(self.logFileName, 'w')
        logfile.write(writeLogDetail)
        logfile.close()

    def logAdd(self, addLogDetail):
        logfile = open(self.logFileName, 'a')
        logfile.write(addLogDetail)
        logfile.close()
