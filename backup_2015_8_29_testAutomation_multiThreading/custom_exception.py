import exceptions
class TimeOut_Error(Exception):
    def __TimeOut__(self, expect):
        print "TimeOut when waiting for: " + expect


class EOF_Error(Exception):
    def __EOF__(self, expect):
        print "EOF when waiting for: " + expect


class Fault_Error(Exception):
    def __Fault__(self):
        print "Some error occured!"