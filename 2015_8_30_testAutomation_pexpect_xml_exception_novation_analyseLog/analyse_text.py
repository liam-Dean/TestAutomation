# -*- coding:utf-8 -*-
import os
from read_xml_config import ReadXMLConfig

def analyseRTBInSv(logName, fileFormat, destination):
    analyseFile = open(logName)
    status = ""
    for line in analyseFile.readlines():
        line.strip()
        if not len(line) or line.startswith('#'):       # pass the blank line
            continue
        target1 = line.find(fileFormat)
        target2 = line.find(destination)
        if target1 != -1 & target2 != -1:
            if line.find  ("INSV") != -1:
                status = "INSV"
            elif line.find("SYSB") != -1:
                status = "SYSB"
            elif line.find("OFFL") != -1:
                status = "OFFL"
            elif line.find("ISTB") != -1:
                status = "ISTB"
            elif line.find("MANB") != -1:
                status = "MANB"
            else:
                status = "Not Found"
            break
        else:
            status = "Could match the configuration"
    return status

def analyseConfRTBConfigurated(logName, fileFormat, destination):
    analyseFile = open(logName)
    status = ""
    for line in analyseFile.readlines():
        line.strip()
        if not len(line) or line.startswith('#'):       # pass the blank line
            continue

        target1 = line.find(fileFormat)
        target2 = line.find(destination)
        if target1 != -1 & target2 != -1:
            if line.find("CONFIGURED") != -1:
                status = "CONFIGURED"
            elif line.find("UNCONFIGURED") != -1:
                status = "UNCONFIGURED"
            else:
                status = "Not Found"
            break
        else:
            status = "Could match the configuration"

    return status

def analyseScheduleInfo(logName, configStream, configFileFormat, configDestination, configFileDestination):
    analyseFile = open(logName)
    stream = ""
    fileFormat = ""
    destination = ""
    fileDestination = ""
    for line in analyseFile.readlines():
        line.strip()
        if not len(line) or line.startswith('#'):       # pass the blank line
            continue

        if line.find("Stream") != -1:
            index = line.find(":")
            stream = line[index + 3:line.find("'", index + 3)]
            if stream == configStream:
                pass
            else:
                stream = ""

        elif line.find("Format_Type") != -1:
            index = line.find(":")
            fileFormat = line[index + 3:line.find("'", index + 3)]
            if fileFormat == configFileFormat:
                pass
            else:
                fileFormat = ""


        elif (line.find("Destination") != -1) & (line.find("_Destination") == -1):
            index = line.find(":")
            destination = line[index + 3:line.find("'", index + 3)]
            if destination == configDestination:
                pass
            else:
                destination = ""

        elif line.find("Remote_Storage_Directory") != -1:
            index = line.find(":")
            fileDestination = line[index + 3:line.find("'", index + 3)]
            if fileDestination == configFileDestination:
                pass
            else:
                fileDestination = ""

        else:
            pass

        if (stream != "") & (fileFormat != "") & (destination != "") & (fileDestination != ""):
            verify = "success"
            return verify
    verify = "failed"
    return verify

def analyseBillingList(logName):
    analyseFile = open(logName)
    lastestLine = ""
    lastestNum = ""
    flag = 0
    for line in analyseFile.readlines():
        line.strip()
        if not len(line) or line.startswith('#'):       # pass the blank line
            continue
        if line.find("AMA") != -1:
            flag = 1
            pass
        elif (flag == 1) & (line.find("AMA") == -1):
            index = lastLine.find("AMA")
            lastestNum = lastLine[index - 2:index]
            return lastestNum
        else:
            lastestNum = 0
        lastLine = line

    return lastestNum

def checkResult(step1Result,step2Result,step3Result,step4Result,step5Result):
    if step1Result | step2Result | step3Result | step4Result | step5Result == 0:
        print "\033[1;36;40m***Test success!***\033[0m"

    if step1Result != 0:
        print "\033[1;31;40m***Some error occured at Step1***\033[0m"

    if step2Result != 0:
        print "\033[1;31;40m***Some error occured at Step2***\033[0m"

    if step3Result != 0:
        print "\033[1;31;40m***Some error occured at Step3***\033[0m"

    if step4Result != 0:
        print "\033[1;31;40m***Some error occured at Step4***\033[0m"

    if step5Result != 0:
        print "\033[1;31;40m***Some error occured at Step5***\033[0m"


if __name__ == '__main__':
    config = ReadXMLConfig('config_case1.xml').xmlGetTagAsDictionary() # Load the configuration
    path = os.path.join(os.path.join(os.getcwd(), "Log"), "log3.log")
    stream, fileFormat, destination, fileDestination = analyseScheduleInfo(path, config["stream"], config["fileFormat"],
                                                                           config["destination"],
                                                                           config["fileDestination"])
    print stream, fileFormat, destination, fileDestination
    path = os.path.join(os.path.join(os.getcwd(), "Log"), "log1.log")
    status = analyseRTBInSv(path, fileFormat, destination)
    print status
    path = os.path.join(os.path.join(os.getcwd(), "Log"), "log2.log")
    config = analyseConfRTBConfigurated(path, fileFormat, destination)
    print config
    path = os.path.join(os.path.join(os.getcwd(), "Log"), "log4.log")
    lastestNum = analyseBillingList(path)
    print lastestNum
