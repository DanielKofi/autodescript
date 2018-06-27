import csv
import netmiko
import getpass
from netmiko import ConnectHandler
import time
import sys


last_ip = ''
with open('portdescript.csv', 'r') as f:
     readCSV = csv.reader(f, delimiter=',')
     for row in readCSV:
        #grab variables from csv
        outlet = row[0]
        des = row[1]
        ip = row[2]
        sw = row[3]
        port = row[4]
        
        #fullDess = outlet number and description i.e "3201/8 Wifi"
        fullDes = '{}{}{}{}{}'.format(outlet,' ','-',' ',des)
        if des == '':
            #if the descritipon row is empty, just use the oulet number for the description
            fullDes = '{}'.format(outlet)
       
        #create interface string i.e. 'gi2/0/4'
        intFace = '{}{}{}{}'.format('gi',sw,'/0/',port)
        print('Configuring ',ip)

        if last_ip != ip:
            print('entering loop with',ip)
            try:
                time.sleep(1)
                print('checking please wait........')
                conn = ConnectHandler(device_type='cisco_ios'
                                     ,ip = ip
                                     ,username='xxxxxx'
                                     ,password='xxxxxx'
                                     ,secret='xxxxxxx')
            except:
                print('cound not connect to',ip)
                with open('switchfails.txt','w') as f:
                    f.write('script could not log into ' + ip)

            last_ip = ip

        conn.enable()
        conn.config_mode()
            
        cmd = ['int {}'.format(intFace),'des {}'.format(fullDes)
        out = conn.send_config_set(cmd)
        if 'Invalid input'in out:
           print('if loop')
           cmd = ['int fa0/{}'.format(port),'des {}'.format(fullDes)]
           print(cmd)
     


