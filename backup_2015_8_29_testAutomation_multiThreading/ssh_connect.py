# -*- coding:utf-8 -*-
__author__ = 'ezhicdi'

import paramiko,sys,traceback
from paramiko.py3compat import input
try:
    import ssh_interactive
except ImportError:
    from . import ssh_interactive

class ssh:
    def __init__(self,hostname,username,password,port=22):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port
        self.client = ''
        self.chan = ''

    def connect(self):
        # now, connect and use paramiko Client to negotiate SSH2 across the connection
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('***Connecting***')

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                self.client.close()
            except:
                pass
            sys.exit(1)

    def execute_command(self,commands):
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            print stdout.readlines()

    def interactive_shell(self):
        self.chan = self.client.invoke_shell()
        print('*** interactive!\n')
        interactive.interactive_shell(self.chan)

    def disconnect(self):
        self.chan.close()
        self.client.close()
        print "***disconnect!***"