# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'
import os,os.path
class log:
    def __init__(self,name,mode='r'):
        self.name=name
        self.mode=mode
        self.dir=os.getcwd()
        self.logDir=os.path.join(self.dir,"Log")
        self.logFileName=os.path.join(self.logDir,self.name)
        self.logFile()

        if os.path.exists(self.logDir):#Make the path  if it doesn't exist
            pass
        else:
            os.mkdir(self.logDir)

    def logFile(self):
        self.logfile=open(self.logFileName,self.mode)
        return self.logfile

    def keyLogWrite(self,comment=" "):
        logfile = open(self.logFileName, 'w')
        logfile.write(comment)

    def keyLogAdd(self,before,after=None):
        logfile = open(self.logFileName, 'a')
        logfile.write(before)
        logfile.write(after)


