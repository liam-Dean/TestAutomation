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
