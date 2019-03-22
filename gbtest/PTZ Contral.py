#! /usr/bin/env python
#-*- coding: UTF-8 -*-

from Tkinter import *
import re
import sys
import pjsua as pj
import copy
import random
from random import randrange
import threading
import time

#########################################pjsip###################################
LOG_LEVEL = 3

def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

lib = pj.Lib()

lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))

transport = lib.create_transport(pj.TransportType.UDP,pj.TransportConfig(0))
print "\nListening on", transport.info().host,
print "port",transport.info().port, "\n"

lib.start()

acc = lib.create_account_for_transport(transport, cb=MyAccountCallback())
acc.set_basic_status(True)

my_sip_uri = "sip:" + transport.info().host + \
            ":" + str(transport.info().port)
print "My SIP URI is", my_sip_uri

################################### globel #######################################
URI = ""
pattern = "^sip:((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d{0,5}$"
R_PTZ = "A50F01011F0000D5"
L_PTZ = "A50F01021F0000D6"
T_PTZ = "A50F0108001F00DC"
D_PTZ = "A50F0104001F00D8"
S_PTZ = "A50F0100000000B5"
O_PTZ = "A50F0110000010D5"
I_PTZ = "A50F0120000010E5"

################################### function #####################################
def setup():
    lib.thread_register("t")
    user = 'sip:10.69.2.60:5070'
    #user = input("please input ip:")
    if re.match(pattern,user):
        global URI 
        URI = user.rstrip("\r\n")
    x=randrange(1,8)
    if x==1:
        print 'left'
        left()
    elif x==2:
        print 'right'
        right()
    elif x==3:
        print 'top'
        top()
    elif x==4:
        print 'down'
        down()
    elif x==5:
        print 'out'
        outt()
    elif x==6: 
        print 'in'
        inn()
    else:
		print 'zoom'
		zoom()

    t = threading.Timer(20, setup)
    t.start()


if __name__ == "__main__":
    lib.thread_register("t")
    t = threading.Timer(10, setup)
    t.start()


def getParse(flag, ptz, num):
    first_byte = ptz[0:2]
    code1 = ptz[2:4]
    addr = ptz[4:6]
    instruction = ptz[6:8]
    data1 = ptz[8:10]
    data2 = ptz[10:12]
    code2 = ptz[12:14]

    if flag == 1:#left
        instruction = "02"
        data1 = num
    
    elif flag == 2:#right
        instruction = "01"
        data1 = num

    elif flag == 3:#up
        instruction = "08"
        data2 = num

    elif flag == 4:#down
        instruction = "04"
        data2 = num

    elif flag == 5:#out
        instruction = "10"
        code2 = num + '0'

    elif flag == 6:#in
        instruction = "20"
        code2 = num + '0'
    
    ifirst_byte = int(first_byte,16)
    icode1 = int(code1,16)
    iaddr = int(addr,16)
    iinstruction = int(instruction,16)
    idata1 = int(data1,16)
    idata2 = int(data2,16)
    icode2 = int(code2,16)
    check_code = (ifirst_byte+icode1+iaddr+iinstruction+idata1+idata2+icode2)%256
    print check_code 
    check_code = hex(check_code)[2:].upper()
    print check_code
    if len(check_code) == 1:
        check_code = '0' + check_code

    ptz_temp = first_byte + code1 + addr + instruction + data1 + data2 + code2 + check_code
    
    if flag == 1:#left
        global L_PTZ
        L_PTZ = ptz_temp

    elif flag == 2:#right
        global R_PTZ
        R_PTZ = ptz_temp
      

    elif flag == 3:#up
        global T_PTZ
        T_PTZ = ptz_temp
    

    elif flag == 4:#down
        global D_PTZ
        D_PTZ = ptz_temp
  

    elif flag == 5:#out
        global O_PTZ
        O_PTZ = ptz_temp


    elif flag == 6:#in
        global I_PTZ
        I_PTZ = ptz_temp

def left():
    dec = 50
    num = hex(dec)[2:].upper()
    if len(num) == 1:
        num = '0' + num
    print num
    global L_PTZ
    getParse(1,L_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + L_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

def right():
    dec = 50
    num = hex(dec)[2:].upper()
    if len(num) == 1:
        num = '0' + num
    print num
    global R_PTZ
    getParse(2,R_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + R_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

def top():
    dec = 50
    num = hex(dec)[2:].upper()
    if len(num) == 1:
        num = '0' + num
    print num
    global T_PTZ
    getParse(3,T_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + T_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

def down():
    dec = 50
    num = hex(dec)[2:].upper()
    if len(num) == 1:
        num = '0' + num
    print num
    global D_PTZ
    getParse(4,D_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + D_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

def outt():
    dec = 7
    num = hex(dec)[2:].upper()
    print num
    
    global O_PTZ
    getParse(5,O_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + O_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")
    
def inn():
    dec = 7
    num = hex(dec)[2:].upper()
    print num
    
    global I_PTZ
    getParse(6,I_PTZ,num)
    print URI
    data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>11</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<PTZCmd>" + I_PTZ + "</PTZCmd>\n</Control>"
    acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

def zoom():
	print URI
	data = "<?xml version=\"1.0\"?>\n<Control>\n<CmdType>DeviceControl</CmdType>\n<SN>17430</SN>\n<DeviceID>34020000001320000001</DeviceID>\n<DragZoomOut>\n<Length>1080</Length>\n<Width>1920</Width>\n<MidPointX>960</MidPointX>\n<MidPointY>540</MidPointY>\n<LengthX>100</LengthX>\n<LengthY>100</LengthY>\n</DragZoomOut>\n</Control>"
	acc.send_pager(URI,data,0,"Application/MANSCDP+xml")

