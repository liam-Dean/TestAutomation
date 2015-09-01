#!/usr/bin/env python
# -*- coding:utf-8 -*-
import test_automation
if __name__ == '__main__':
    #devices config
    cbm = {'name': 'GSM_T4_CBM_HA',
           'clusterIP': '10.178.28.35',
           'clusterUser': 'nortel',
           'clusterPasswd': 'nortel',
           'clusterRootUser': 'root',
           'clusterRootPasswd': 'root',
           'unit0IP': '10.178.28.27',
           'unit1IP': '10.178.28.28',
           'consoleIP': '10.178.33.8',
           'consoleUser': 'admin',
           'consolePasswd': 'admin',
           'consoleUnit0Port':'7028',
           'consoleUnit1Port': '7027'
           }

    core={'name': 'Sanity_10.24.16.134',
          'ip': '10.24.16.134',
          'user': "lisa",
          'passwd': 'lisa'
          }

    server={'name': 'Server_202.38.35.184',
            'ip': '202.38.35.184',
            'user': 'bsmbin',
            'passwd': 'Abcde01!'
            }

    configuration = {'stream': 'AMA',
                     'fileFormat': 'DIRP',
                     'destination': 'TEST',
                     'essentialDestination': 'YES',
                     'protocol': 'RSFTP',
                     'primaryDestination': '202.38.35.184',
                     'primaryPort': '22',
                     'alternateDestination': '202.38.35.184',
                     'alternatePort': '22',
                     'startTime': '00:00',
                     'stopTime': '23:59',
                     'interval': '5',
                     'remoteStorageDirectory': '/export/home/bsmbin/lisa/billing4',
                     'remoteLogin': server["user"],
                     'remotePassword': server["passwd"],
                     'maximumRetries': '3',
                     'retryWaitTime': '1',
                     'fileExtension': '',
                     'fieldSeparator': '.',
                     'active': 'No'
                     }

    rtbStatus = ['INSV', 'SYSB', 'OFFL', 'ISTB', 'MANB']
    rtbStatus2 = ['CONFIGURED', 'UNCONFIGURED']
    rtbProtocal = ['FTPW', 'RFTPW', 'SFTPW', 'KSFTP', 'RSFTP', 'RKSFT']


