__author__ = 'ezhicdi'
import  xml.dom.minidom
def read_Config(CBM,Core,Server):
    dom = xml.dom.minidom.parse('Config_Case1.xml')
    root = dom.documentElement
    device=dom.getElementsByTagName("Host")
    CBM["hostname"]   = device[0].firstChild.data
    Core["hostname"]  = device[1].firstChild.data
    Server["hostname"]= device[2].firstChild.data

    device=dom.getElementsByTagName("User")
    CBM["username"]   = device[0].firstChild.data
    Core["username"]  = device[1].firstChild.data
    Server["username"]= device[2].firstChild.data

    device=dom.getElementsByTagName("Passwd")
    CBM["password"]   = device[0].firstChild.data
    Core["password"]  = device[1].firstChild.data
    Server["password"]= device[2].firstChild.data

    device=dom.getElementsByTagName("Port")
    CBM["port"]   = device[0].firstChild.data
    Core["port"]  = device[1].firstChild.data
    Server["port"]= device[2].firstChild.data

    device = dom.getElementsByTagName("Protocal")
    CBM["protocal"] = device[0].firstChild.data
    Core["protocal"] = device[1].firstChild.data
    Server["protocal"] = device[2].firstChild.data

    device = dom.getElementsByTagName("RootPasswd")
    CBM["RootPassword"]=device[0].firstChild.data



    return CBM,Core,Server