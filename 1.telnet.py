import telnetlib


def do(ip,user,password,commands):
    tn = telnetlib.Telnet(ip)
    tn.set_debuglevel(2)

    tn.read_until("login: ")
    tn.write(user + "\n")
    tn.read_until("Password: ")
    tn.write(password + "\n")

    for command in commands:
        tn.write(command+"\n")
    
    tn.write("exit\n")
    print tn.read_all()
   
    print "Finish"

ip="192.168.191.136"
user="jason"
password="996633"
commands=["cd /home", "ls"]
do(ip,user,password,commands)