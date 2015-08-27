import paramiko

def ssh_cmd(ip,port, cmd, user, passwd):
    result = ""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, passwd,timeout=3)
        stdin, stdout, stderr =ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
    except:
        print("ssh_cmd err.")
    return result

ip="192.168.191.136"
port=22
user="jason"
passwd="996633"
cmd="ls"
result=ssh_cmd(ip,port, cmd, user, passwd)

file_object=open('result.txt','wb')
file_object.write(result)
file_object.close()
print ('Finish')
