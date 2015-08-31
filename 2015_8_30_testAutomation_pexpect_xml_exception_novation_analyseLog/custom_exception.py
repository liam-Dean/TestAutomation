import exceptions

class TimeOutError(Exception):
    def __TimeOut__(self, expect):
        print "TimeOut when waiting for: " + expect

class EndOfFileError(Exception):
    def __EOF__(self, expect):
        print "EOF when waiting for: " + expect

class FaultError(Exception):
    def __Fault__(self):
        print "Some error occured!"

class TextTraverseError(Exception):
    def __TraverseError__(self):
        pass

class TextAnalyseError(Exception):
    def __AnalyseError__(self):
        print "Analyse failed!"

class RTBInSvError(Exception):
    def __init__(self, stream, fileFormat, destination, status):
        self.stream=stream
        self.fileFormat=fileFormat
        self.destination=destination
        self.status = status

    def __RTBInSvError__(self):
        print "%s %s %s \033[1;31;40m %s \033[0m" %(self.stream,self.fileFormat,self.destination,self.status)

class RTBConfigurationError(Exception):
    def __init__(self, stream, fileFormat, destination, config):
        self.stream=stream
        self.fileFormat=fileFormat
        self.destination=destination
        self.config = config

    def __RTBConfigurationError__(self):
        print "%s %s %s \033[1;31;40m %s \033[0m" %(self.stream,self.fileFormat,self.destination,self.config)

class ScheduleError(Exception):
    def __init__(self, stream, fileFormat, destination, fileDestination):
        self.stream = stream
        self.fileFormat = fileFormat
        self.destination = destination
        self.fileDestination = fileDestination

    def __ScheduleError__(self):
        print "Couldn't match the configuration: stream:%s " \
              "                                  File_Format_Type:%s " \
              "                                  Destination:%s " \
              "                                  Remote_Storage_Directory:%s "\
              % (self.stream, self.fileFormat, self.destination, self.fileDestination)



