import xml.dom.minidom
class ReadXMLConfig():
    def __init__(self, path):
        self.path = path
        self.dom = xml.dom.minidom.parse(self.path)
        self.dataString = self.dom.toprettyxml().encode("UTF-8")

    '''
        Traverse the xml and return it as a string
    '''

    def xmlToString(self):
        return self.dataString

    '''
        Transfer the string of the xml to a dictionary
    '''

    def xmlGetTagAsDictionary(self):
        structTag = {}
        splitedParts = self.dataString.split("\n\t\n")
        for splitedPart in splitedParts:
            if splitedPart.find("<") != -1 and splitedPart.find("/>") != -1:
                structName = splitedPart[splitedPart.find("<") + 1:splitedPart.find(" value")]
                structValue = splitedPart[splitedPart.find('\"') + 1:splitedPart.find('\"', splitedPart.find('\"') + 1)]
                structTag[structName] = structValue
        return structTag