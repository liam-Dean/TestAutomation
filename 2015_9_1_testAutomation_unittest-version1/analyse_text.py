# -*- coding:utf-8 -*-
def lastLine(filePath, pos):
    file = open(filePath, 'rb')
    while True:
        pos = pos - 1
        try:
            file.seek(pos, 2)
            if file.read(1) == '\n':
                break
        except:
            file.seek(0, 0)
            print file.readline().strip()
            return
    lineString = file.readline().strip()
    file.close()
    return lineString, pos

def getRTBStatus1(filePath, fileFormat, destination):
    analyseFile = open(filePath)
    status = " "
    for line in analyseFile.readlines():
        line.strip()
        if not len(line) or line.startswith('#'):       # pass the blank line
            continue
        target1 = line.find(fileFormat)
        target2 = line.find(destination)
        if target1 != -1 & target2 != -1:
            if line.find("INSV") != -1:
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

def getRTBStatus2(filePath, fileFormat, destination):
    analyseFile = open(filePath)
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

def getRTBConfig(filePath, configStream, configFileFormat, configDestination, configFileDestination):
    analyseFile = open(filePath)
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

def getLastFileNumber(filePath):
    pos = 0
    analyseFile = open(filePath, "rU")
    count = len(analyseFile.readlines())
    analyseFile.close()
    for i in range(count):
        lineString, pos = lastLine(filePath, pos)
        if lineString.find("AMA") != -1:
            break
    lastFileNum = long(lineString[lineString.find('U') + 1:lineString.find('AMA')])
    return lastFileNum

def getLastFileName(filePath):
    pos = 0
    analyseFile = open(filePath, "rU")
    count = len(analyseFile.readlines())
    analyseFile.close()
    for i in range(count):
        lineString, pos = lastLine(filePath, pos)
        if lineString.find("AMA") != -1:
            break
    lastFileName = long(lineString[lineString.find('U'):lineString.find('AMA')+3])
    return lastFileName
