#! /usr/bin/env python
# _*_ coding: UTF-8 _*_ 
# Filename: ProtocolCtrl.py

import os
from Tkinter import *
import socket, traceback
import ttk
import datetime
import webbrowser
import tkSimpleDialog
import tkFileDialog
import sys                #python 2.x 默认编码是ascii格式; python 3.x 默认编码是utf-8格式
reload(sys)
sys.setdefaultencoding('utf-8')



root = Tk()
#生成一个底层窗口
#root.geometry('450x400')
#窗口大小
root.resizable(True, True)
#是否可以左右上下拉框放大缩小
root.attributes("-alpha",0.6)
#窗口透明度百分之四十
root.title('mangotest')
#窗口标题


onvifDict = {
    'onvifBin' : 'mantisONVIFServer',
	'logDir'	: '/var/tmp/aqueti/',
	'onvifLog'	: 'Log/',
	'runLog'	: 'onvifRun',
	'onvifLogoFile' : './logo/onvifLogo.png',
	'rtspIpAddr' : '',
	'rtspPort' : '17100',
	'onvifPort' : '21100',
	'HW1080P'	: '1080 * 1920',
	'HW4K'		: '2160 * 3840',
	'HWCustom'	: 'high * width',
	'imgQuality' :	'0.5',
	'EncDef'    : '0',
	'ResDef'    : '0',
	'RootDef'   : '0',
	'RecordDef' : '1',
	'CropDef'   : '0'
	}

modelDict = {
	'modleLogoFile' : './logo/modelCtrl.png',
	'DefModelPath'	: '/var/tmp/aqueti/modelgen/',
	'RenderServer'  : '',
	'NickName'      : '78',
	'ModelFile'		: 'model.json',
	'ModelEdit'		: 'model_edited.json',
	'CustomModel'	: 'model_custom.json',
	'ModelPagoda'	: 'model_pagoda.json',
	'ModelPanoLH'	: 'model_panorama_lh.json',
	'ModelPanoFH'	: 'model_panorama_fh.json'
	}	

daemonDict = {
	'configuration'	:	'/etc/aqueti/daemonConfiguration.json',
	'protocolCtrl'	:	'/etc/aqueti/ProtocolCtrl/ProtocolCtrl2.py'
}


ptzDict = {
	'tourDefault'	: "2, (0 / 1 / 1.2)",
	'tourDefault1'	: "11, (0 / 1.2 / 1.2)",
	'tourDefault2'	: "11, (0 / -1.2 / 0.8)",
	'PTZLeft'	: './logo/left.png',
	'PTZRight'	: './logo/right.png',
	'PTZUp'		: './logo/up.png',
	'PTZDown'	: './logo/down.png',
	'PTZIn'		: './logo/ZoomIn.png',
	'PTZOut'	: './logo/ZoomOut.png',
	'PTZStop'	: './logo/stop.png',
	'PTZHome'	: './logo/home.png',
	'Play'		: './logo/play.png',
}



# 28181 cmd/cfg para define
gbCfgListChinese = ('服 务 器 编 码:', '服务器 IP地址:', '服 务 器 端 口:', '用户认 证编码:', '监  听   端  口:', '用     户     名:', '密             码:', '服务器      ID:','报警通 道编码:', '视频通 道编码:', '注 册 有 效 期:')
gbCfgList = ('server_id', 'server_ip', 'server_port', 'device_id', 'listen_port', 'username', 'password','cameral_system', 'alarm_id', 'media_id', 'register_expire')
gbDict =  {
	'gbCfgFileName' : '/etc/aqueti/GB/mantisGBprofile.conf',
	'gbCfgFileDir' : '/etc/aqueti/GB/',
	'gbBin' : 'mantisGBclient &',
	'gbLogoFile' : './logo/gb28181Logo.png'
	}

gbCfgFilePrefix = '{\n  "keepalive_timeout":10,\n  "re-register_timeout":60,\n  "keepalive_timeout_num":3,\n  "local_ip":"",\n  "local_port":5890,\n  "user_profile":{\n'
gbCfgFileSuffix ='  }\n}'


helpDocDict = {
	'onvifHelp' : './help/ONVIF安装使用手册.pdf',
	}

maintainDict = {
	'ntpCheck'	: "sudo ntpq -p;exit",
	'ntpSync'	: """sudo service ntp stop; sudo ntpd -gq; sudo service ntp start; sudo ntpq -p;exit""",
	'daemonCheck'	: "sudo service Aqueti-Daemon status;exit",
	'daemonRes'	: "sudo service Aqueti-Daemon restart;exit"
}

logDirDict = {
	'logInfo'		:	'~/LogInfo',
	'mantisInfo'	:	'~/LogInfo/mantis',
	'renderInfo'	:	'~/LogInfo/render',
	'onvifInfo'		:	'~/LogInfo/onvif'
}

mantisLogDict = {
	'syslog'	: 	'/var/log/syslog',
	'acosd.err'	:	'/var/log/acosd.err',
	'acosd.out'	:	'/var/log/acosd.out'
}

renderLogDict = {
	'syslog'	:	'/var/log/syslog*',
	'web'	:	'/var/log/aqueti/homunculus-stdout*',
	'mongodb'	:	'/var/log/mongodb/mongod.log',
	'model.json'	:	'/var/tmp/aqueti/modelgen/model.json'
}

onvifLogDict = {
	'runLog'	:	'/var/tmp/aqueti/Log',
	'xmlCfg'	:	'/var/tmp/aqueti/*.xml'
}

simpleDialogDict = {
	'pagoda'	: '',
	'panoLH'	: '',
	'panoFH'	: '',
	'custom'	: '',
	'InitModel'	: '恢复模型到初始状态\n1.删除用户定义的模型文件\n2.时间戳信息不会还原\n',
	'ReinstallOnvif'	: '重新安装ONVIF版本\n覆盖安装工具配套的ONVIF版本\n'
}


LisenceNotice = '''***************************************************************************************
 *
 *  重要提示：在下载、复制、安装或使用之前请阅读。
 *
 *  版权所有 (C) 2018, Aqueti Inc, 保留所有权利.
 *
****************************************************************************************'''

FunctionNotice = '''***************************************************************************************
 *
 * ONVIF
 * 	1. 设置onvif启动参数
 *	2. 启动onvif
 *	3. 录像控制、PTZ控制
 * Tour
 *	1. 预置位设置
 *	2. 开始、关闭巡航
 * MODEL
 *	1. 选择模型文件
 *	2. 修改模型文件
 * GB28181
 *	1. gb28181参数设置
 *	2. 启动gb28181
 *
****************************************************************************************'''

ContactNotice = '''***************************************************************************************
 *
 * limin
 * 2019-03-18
 * limin@aqueti.com
 *
****************************************************************************************'''


# photo define
modleLogo = PhotoImage(file=modelDict['modleLogoFile'])
VideoPlay = PhotoImage(file=ptzDict['Play'])
onvifLogo = PhotoImage(file=onvifDict['onvifLogoFile'])
PTZLeft = PhotoImage(file=ptzDict['PTZLeft'])
PTZRight = PhotoImage(file=ptzDict['PTZRight'])
PTZUp = PhotoImage(file=ptzDict['PTZUp'])
PTZDown = PhotoImage(file=ptzDict['PTZDown'])
PTZIn = PhotoImage(file=ptzDict['PTZIn'])
PTZOut = PhotoImage(file=ptzDict['PTZOut'])
PTZStop = PhotoImage(file=ptzDict['PTZStop'])
gbLogo = PhotoImage(file=gbDict['gbLogoFile'])
PTZHome = PhotoImage(file=ptzDict['PTZHome'])

def quit_window():
	root.quit()
	root.destroy()
	exit()


#onvif

def get_host_ip():
    try:
		if onvifDict['rtspIpAddr'] != '':
			return onvifDict['rtspIpAddr']
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
		s.close()
		return ip
    except socket.error, e:
		print  e
		traceback.print_exc()
		return '127.0.0.1'
		
def getRenderServerID(filepath):
	if modelDict['RenderServer'] != '':
		return modelDict['RenderServer']
	serverIDName = "system"
	with open(filepath, "r") as f:
		for line in f:
			if serverIDName in line:
				serverID = line.split('\"')[3].strip()
				return "aqt://" + serverID
	return modelDict['RenderServer']



def click_start_onvif(sudo, rip, rp, op, enc, res, render, nn, record, qua, crop):
	print "click_start_onvif", sudo, rip, rp, op, enc, res, render, nn, record, qua, crop

	if sudo:
		start_onvif_commad = 'sudo ' + onvifDict['onvifBin']
	else:
		start_onvif_commad = onvifDict['onvifBin']
	if '' == rip.strip():
		start_onvif_commad += ' -rip ' + onvifDict['rtspIpAddr']
	else:
		start_onvif_commad += ' -rip ' + rip
	if '' == rp.strip():
		start_onvif_commad += ' -rp ' + onvifDict['rtspPort']
	else:
		start_onvif_commad += ' -rp ' + rp
	if '' != op.strip():
		start_onvif_commad += ' -op ' + op
	if 'h264' == enc.strip():
		start_onvif_commad += ' -h264'
	elif 'JPEG' == enc.strip():
		start_onvif_commad += ' -JPEG'
	else:
		start_onvif_commad += ' -h265'
	if onvifDict['HW1080P'] == res.strip():
		start_onvif_commad += ' -res 1080 1920'
	elif onvifDict['HW4K'] == res.strip():
		start_onvif_commad += ' -res 2160 3840'
	else:
		start_onvif_commad += ' -res '
		start_onvif_commad += res.split('*')[0].strip()
		start_onvif_commad += ' '
		start_onvif_commad += res.split('*')[1].strip()
	if '' != render.strip():
		start_onvif_commad += ' -Render ' + render
	if '' != nn.strip():
		start_onvif_commad += ' -NickName ' + nn
	start_onvif_commad += ' -Record '
	if record:
		start_onvif_commad += '1'
	else:
		start_onvif_commad += '0'
	if '' != qua.strip():
		start_onvif_commad += ' -qua ' + qua
	if crop:
		start_onvif_commad += ' -crop'
	start_onvif_commad += '| tee ' 
	start_onvif_commad += onvifDict['logDir'] + onvifDict["onvifLog"] +  onvifDict["runLog"]
	start_onvif_commad += modelDict["NickName"] + '_'
	start_onvif_commad += datetime.datetime.now().strftime('%Y%m%d.%H:%M:%S')
	start_onvif_commad += ' &'

	print ('Start onvifServer CMD [' + start_onvif_commad + "]")
	# start onvifServer
	if os.system(start_onvif_commad) == 0:
		print 'Successful START onvifServer on', start_onvif_commad
	else:
		print 'START onvifServer Completed'

def CtrlRecord(ip, op, action):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'startRecord Connect', ip, op, 'success!'
		cmdStr = 'Record ';
		if 'start' == action.strip():                                   #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
			cmdStr += 'START'
		else:
			cmdStr += 'STOP'
		cmdStr += ' record\r\n'
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		'''
		wait rsp
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()

def restoreCfg():
	lineNum = 0
	with open (daemonDict['protocolCtrl'], "r") as f:
		lines = f.readlines()
	with open (daemonDict['protocolCtrl'], "w") as f_w:
		for line in lines:
			lineNum += 1
			if lineNum < 300:
				if "'rtspIpAddr' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'',")
					print line
				if "'rtspPort' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'17100',")
					print line
				if "'onvifPort' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'21100',")
					print line
				if "'EncDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'0',")
					print line
				if "'ResDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'0',")
					print line
				if "'imgQuality' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'0.5',")
					print line
				if "'RootDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'0',")
					print line
				if "'RecordDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'1',")
					print line
				if "'RenderServer' " in line:
					value = line.split(':')[0]
					line = value + ": '',\n"
					print line
				if "'NickName' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'70',")
					print line
				if "'RootDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'0',")
					print line
			f_w.write(line)
	print "restore cfg to default success"

def saveAsDefultCfg(CB, IP, RP, OP, enc, res, system, NName, Record, qua, crop):
	print CB, IP, RP, OP, enc, res, system, NName, Record, crop
	lineNum = 0
	with open (daemonDict['protocolCtrl'], "r") as f:
		lines = f.readlines()
	with open (daemonDict['protocolCtrl'], "w") as f_w:
		for line in lines:
			lineNum += 1
			if lineNum < 300:
				if "'rtspIpAddr' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ IP + "',")
					print line
				if "'rtspPort' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ RP + "',")
					print line
				if "'onvifPort' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ OP + "',")
					print line
				if "'EncDef' " in line:
					if 'h264' == enc.strip():
						encNum = '0'
					elif 'JPEG' == enc.strip():
						encNum = '1'
					else:
						encNum = '2'
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ encNum + "',")
					print line
				if "'ResDef' " in line:
					if onvifDict['HW1080P'] == res.strip():
						resNum = '0'
					elif onvifDict['HW4K'] == res.strip():
						resNum = '1'
					else:
						resNum = '2'
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ resNum + "',")
					print line
				if "'imgQuality' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ qua + "',")
					print line
				if "'RootDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ str(CB) + "',")
					print line
				if "'RecordDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ str(Record) + "',")
					print line
				if "'RenderServer' " in line:
					value = line.split(':')[0]
					line = value + ": '" + system + "',\n"
					print line
				if "'NickName' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ NName + "',")
					print line
				if "'CropDef' " in line:
					value = line.split(':')[1].strip()
					line = line.replace(value, "'"+ str(crop) + "',")
					print line
			f_w.write(line)
	print "save cur cfg ad default success"	

def vlcPlay(ipAddr, rtpPort, transType):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ipAddr, int(rtpPort)))
		print 'play connect success'
		clientSock.close()
		tansport = ' --no-rtsp-tcp '
		if 'TCP' == transType.strip():
			tansport = ' --rtsp-tcp '
		elif 'UDP' == transType.strip():
			tansport = ' --no-rtsp-tcp '
		elif 'HTTP' == transType.strip():
			tansport = ' --rtsp-http '
		vlc_cmd = 'vlc rtsp://' + ipAddr + ':' + rtpPort + '/onvif/Streaming/channels/101' + tansport +'&'
		os.system(vlc_cmd)
	except OSError:
		print "Can NOT open vlc, Aborted!"
	except socket.error, e:
		print "connect", ipAddr, rtpPort, "failed.", e
		traceback.print_exc()




def click_start_gb():
	# start gbClient
	if os.system(gbDict['gbBin']) == 0:
		print 'Successful START gb28181 client on', gbBin
	else:
		print 'START gb28181 client Completed'

def replace_oldstr_value_from_file(filepath, oldStr, newStrValue):
	with open(filepath, "r") as f:
		for line in f:
			if oldStr in line:
				oldStrvalue = find_old_key_val(line, oldStr)
				if oldStrvalue:
					line = line.replace(oldStrvalue, newStrValue)
				return line


def update_gbcfg_file(filepath, file_content):
	with open(filepath, "w") as f:
		f.write(file_content)

def update_gb_content_dict():
	gb_content_dict = {}
	gb_content_dict['server_id'] = gbSid.get()
	gb_content_dict['server_ip'] = gbSip.get()
	gb_content_dict['server_port'] = gbSpo.get()
	gb_content_dict['device_id'] = gbDid.get()
	gb_content_dict['listen_port'] = gbLpo.get()
	gb_content_dict['username'] = gbUsername.get()
	gb_content_dict['password'] = defgbPwd.get()
	gb_content_dict['cameral_system'] = defgbCam.get()
	gb_content_dict['alarm_id'] = gbAid.get()
	gb_content_dict['media_id'] = gbMid.get()
	gb_content_dict['register_expire'] = gbRex.get()
	return gb_content_dict

				
def update_gb_cfg():
	gbcontent_dict = update_gb_content_dict()
	file_new_data = ''
	for index in range(len(gbCfgList)):
		file_new_data += replace_oldstr_value_from_file(gbDict['gbCfgFileName'], gbCfgList[index], gbcontent_dict[gbCfgList[index]])
	print  file_new_data
	file_content =  gbCfgFilePrefix + file_new_data +  gbCfgFileSuffix
	print file_content
	update_gbcfg_file(gbDict['gbCfgFileName'], file_content)

def vlcPlaygb():
	vlcport = gbport.get()
	vlc_cmd = 'vlc udp://@:'+ vlcport
	os.system(vlc_cmd)

#GB参数
def get_str_value_from_file(filepath, oldStr):
	with open(filepath, "r") as f:
		for line in f:
			if oldStr in line:
				return find_old_key_val(line, oldStr)
		return ''
#得到含有参数哪一行的所有信息，与参数名一起传入find_old_key_val函数中

def check_and_create_file(dirpath, filepath):
	try:
		if not(os.path.exists(dirpath)) and not(os.path.isfile(filepath)):
			os.mkdir(dirpath)
		if not(os.path.exists(filepath) and os.path.isfile(filepath)):
			with open(filepath, 'w') as f:
				file_content =  gbCfgFilePrefix + gbCfgFileSuffix
				f.write(file_content)
	except OSError:
		print ("To detect the uninstalled mantis or GB28181, configure the environment first.")
    	return	
    	
def find_old_key_val(cfgLine, var):
	reStr = '"' + var + '":"(.*)",'         #得到"server_id":"(.*)",信息
	pattern = re.compile(reStr)             
	vallist = pattern.findall(cfgLine)      #以上两步，去除每一条cfgLine中含有"server_id":"(.*)",这些字符的信息，剩下的信息即为vallist列表
	if vallist:
		return vallist[0]
	else:
		reStr = '"' + var + '":(.*),'
		pattern = re.compile(reStr)
		vallist = pattern.findall(cfgLine)
		if vallist:
			return vallist[0]
		else:
			reStr = '"' + var + '":(.*)'
			pattern = re.compile(reStr)
			vallist = pattern.findall(cfgLine)
			if vallist:
				return vallist[0]
			else:
				return ''			

#菜单

def click_check_network():
	try:
		sysinfoCmd = "gnome-system-monitor &"
		os.system(sysinfoCmd)
	except OSError:
		print "open system monitor tool failed"


def click_about_me():
	top = Toplevel()
	top.title("关于")
	LicenseFrame = LabelFrame(top, text=' 许可声明 ', fg = 'green')
	LicenseFrame.grid(row=0, column=0, padx=10, pady=5)
	Label(LicenseFrame, text = LisenceNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)
	FunctionFrame = LabelFrame(top, text=' 软件功能  ', fg = 'green')
	FunctionFrame.grid(row=1, column=0, padx=10, pady=5)
	Label(FunctionFrame, text = FunctionNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)
	ContactFrame = LabelFrame(top, text=' 联系我们 ', fg = 'green')
	ContactFrame.grid(row=2, column=0, padx=10, pady=5)
	Label(ContactFrame, text = ContactNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)

def click_help_onvif():
	top = Toplevel()
	top.title('用户指南')
	Label(top, text='\n请查看软ONVIF安装使用手册,如有问题请联系:li.min@aqueti.com.\n').pack()                #pack布局
	webbrowser.open(helpDocDict['onvifHelp'])

#机头服务

def click_maintain():
	top = Toplevel()
	top.title("检查网络")
	DeviceFrame = LabelFrame(top, text = ' Mantis / Pathfinder ', fg = 'green')
	DeviceFrame.grid(row=0, column=0, padx=10, pady = 10)
	Label(DeviceFrame, text="Tegra 总数", width=12, anchor='e').grid(row=1, column=0, pady=5, sticky=E)
	defTegra = StringVar(); defTegra.set(3);TegraTotal = Entry(DeviceFrame, textvariable=defTegra, width=14).grid(row=1, column=1, pady=5)
	Label(DeviceFrame, text="起始Tegra IP", width=12, anchor='e').grid(row=2, column=0, pady=5, sticky=E)
	defStartIp = StringVar(); defStartIp.set('10.0.1.1');StartIp = Entry(DeviceFrame, textvariable=defStartIp, width=14);StartIp.grid(row=2, column=1, pady=5)
	Button(DeviceFrame, text='检查NTP状态', width=12, height=1, bg='green',\
		command=lambda:maintain(defTegra.get(), StartIp.get(), maintainDict['ntpCheck'])).grid(row=3, column=0,padx=5, pady=5)
	Button(DeviceFrame, text = '同步NTP', width = 12, height = 1, bg = 'green', \
		command=lambda:maintain(defTegra.get(), StartIp.get(), maintainDict['ntpSync'])).grid(row=3,column=1, padx=5, pady=5)
	Button(DeviceFrame, text = '检查机头服务状态', width = 12, height = 1, bg = 'green', \
		command=lambda:maintain(defTegra.get(), StartIp.get(), maintainDict['daemonCheck'])).grid(row=4,column=0, padx=5, pady=5)
	Button(DeviceFrame, text = '重启机头服务', width = 12, height = 1, bg = 'green', \
		command=lambda:maintain(defTegra.get(), StartIp.get(), maintainDict['daemonRes'])).grid(row=4,column=1, padx=5, pady=5)

def maintain(tegraTotal, startIp, cmd):
	try:
		cmdStr = "ssh nvidia@" + startIp + " \"" + cmd + "\""
		print cmdStr
		os.system(cmdStr)
		ipRange = startIp.split('.')
		ipNum = int(ipRange[3])
		ipTotal = int(tegraTotal)
		while ipTotal > 1:
			ipNum += 1
			ip = ipRange[0] + '.' + ipRange[1] + '.' + ipRange[2] + '.' + str(ipNum)
			cmdStr = "ssh nvidia@" + ip + " \"" + cmd + "\""
			print cmdStr
			os.system(cmdStr)
			ipTotal -= 1
	except OSError:
		print "maintain failed!"
	except:
		print 'eeeee'

#查询录像

def queryClip(ip, op):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'queryClip Connect', ip, op, 'success!'
		cmdStr = 'Query Device Info: All Clip\r\n';
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		'''
		wait rsp
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()

def click_queryClip():
	top = Toplevel()
	top.title("录像查询")
	QueryFrame = LabelFrame(top, text = '设备信息', fg = 'green')
	QueryFrame.grid(row=0, column=0, padx=10, pady = 10)
	Label(QueryFrame, text="录像列表", width=12, anchor='e').grid(row=0, column=0, pady=5, sticky=E)
	Button(QueryFrame, text = '查询', width = 12, height = 1, bg = 'green', \
		command=lambda:queryClip(IP.get(), OP.get())).grid(row=0,column=1, padx=10, pady=5)

#日志收集

def infomation_col():
	top = Toplevel()
	top.title("　故障信息收集　")
	# ### 简要描述
	BrifF = LabelFrame(top, text = " 简要描述 (出现了什么问题，错误是什么) ", fg = 'green')
	BrifF.grid(row=0, column=0, padx=10, pady=5, sticky=NW)
	BrifT = Text(BrifF, width=40, height=2);BrifT.grid(row=0, column=0, padx=10, pady=5)
	# ### 详细信息
	DesF = LabelFrame(top, text = "　详细描述　", fg = 'green')
	DesF.grid(row = 1, column = 0, padx=10, pady = 5, sticky = NW)
	# 环境信息 (软硬件和配套操作系统信息)
	envF = LabelFrame(DesF, text = " 环境信息 (软硬件和配套操作系统信息) ")
	envF.grid(row=0, column=0, padx=10, pady=5)
	envI = Text(envF, width = 40, height=2);
	envI.grid(row=0, column=0, padx=5, pady=5)
	# 版本信息 (配套版本的版本信息，被测软件的版本信息)
	verF = LabelFrame(DesF, text = " 版本信息 (配套版本和被测软件的版本信息) ")
	verF.grid(row=1, column=0, padx=10, pady=5)
	verI = Text(verF, width = 40, height=2);
	verI.grid(row=0, column=0, padx=5, pady=5)
	# 重现步骤 ()
	setpF = LabelFrame(DesF, text = " 重现步骤 (重现问题的详细步骤) ")
	setpF.grid(row=2, column=0, padx=10, pady=5)
	setpI = Text(setpF, width = 40, height=4);
	setpI.grid(row=0, column=0, padx=5, pady=5)
	# 预期测试结果 ()
	expF = LabelFrame(DesF, text = " 预期测试结果 ")
	expF.grid(row=3, column=0, padx=10, pady=5)
	expI = Text(expF, width = 40, height=1);
	expI.grid(row=0, column=0, padx=5, pady=5)
	# 实际测试结果 ()
	resuF = LabelFrame(DesF, text = " 实际测试结果 ")
	resuF.grid(row=4, column=0, padx=10, pady=5)
	resuI = Text(resuF, width = 40, height=1);
	resuI.grid(row=0, column=0, padx=5, pady=5)
	# 相关日志 ()
	LogF = LabelFrame(DesF, text = ' 相关日志 ', fg = 'green')
	LogF.grid(row=5, column=0, padx=10, pady=5, sticky=NW)
	# 1. 机头
	mantisLogF = LabelFrame(LogF, text = ' 机头 ')
	mantisLogF.grid(row=0, column=0, padx=10, pady=5, sticky=NW)
	Label(mantisLogF, text = " 收集 ").grid(row=0, column=0,padx=5)
	mantisFlag = IntVar(); mantisFlag.set('1');
	Checkbutton(mantisLogF, variable = mantisFlag, width = 3).grid(row=1, column=0,padx=5,pady=5)
	Label(mantisLogF, text = " Tegra起始IP ").grid(row=0, column=1,padx=5)
	tegraIp = StringVar(); tegraIp.set('10.0.1.1');
	TIP = Entry(mantisLogF, textvariable = tegraIp, width=14); TIP.grid(row=1, column=1, padx=5,pady=5)
	Label(mantisLogF, text = " Tegra数量 ").grid(row=0, column=2,padx=5)
	tegraNum = StringVar(); tegraNum.set('3'); 
	TNum = Entry(mantisLogF, textvariable = tegraNum, width=8);	TNum.grid(row=1, column=2, padx=5,pady=5)
	# 2. render
	renderLogF = LabelFrame(LogF, text = ' 服务器 ')
	renderLogF.grid(row=1, column=0, padx=10, pady=5, sticky=NW)
	Label(renderLogF, text = ' 收集 ').grid(row=0, column=0, padx=5, pady=5)
	renderFlag = IntVar(); renderFlag.set('1');
	Checkbutton(renderLogF, variable = renderFlag, width=3).grid(row=0, column=1, padx=5)
	# 3. onvif
	onvifLogF = LabelFrame(LogF, text = ' ONVIF ')
	onvifLogF.grid(row=2, column=0, padx=10, pady=5, sticky=NW)
	Label(onvifLogF, text = ' 收集 ').grid(row=0, column=0, padx=5, pady=5)
	onvifFlag = IntVar(); onvifFlag.set('1');
	Checkbutton(onvifLogF, variable = onvifFlag, width = 3).grid(row=0, column=1, padx=5)
	recF = LabelFrame(top, text = "")
	# 联系方式
	contactF = LabelFrame(top, text = " 用户联系方式(研发可以直接联系) ", fg= 'green')
	contactF.grid(row=3,column=0, padx=10, pady=5, sticky=NW)
	Label(contactF, text = " 姓名　").grid(row=0, column=0, padx=5, pady=5)
	userName = StringVar(); UN = Entry(contactF, textvariable=userName, width=31);
	UN.grid(row=0, column=1, padx=5, pady=5)
	Label(contactF, text = " 电话　").grid(row=1, column=0, padx=5, pady=5)
	userTel = StringVar(); UT = Entry(contactF, textvariable=userTel, width=31);
	UT.grid(row=1, column=1, padx=5, pady=5)
	Label(contactF, text = " 邮箱　").grid(row=2, column=0, padx=5, pady=5)
	UM = Text(contactF, width = 36, height=1);
	UM.grid(row=2, column=1, padx=5, pady=5)
	Button(top, width=20, height=2, text=' 生成故障信息包 ', bg='green',
		command=lambda:collection_oneKey(mantisFlag.get(), tegraIp.get(), tegraNum.get(), renderFlag.get(), onvifFlag.get(),
		BrifT.get("0.0","end"), envI.get("0.0","end"), verI.get("0.0","end"), 
		setpI.get("0.0","end"), expI.get("0.0","end"), resuI.get("0.0","end"),
		UN.get(), UT.get(), UM.get("0.0","end"))
		).grid(row=4, column=0, padx=10, pady=5)
#.get("0.0","end")获取全部文本

def collection_oneKey(mF, tip, tn, rF, oF, bT, envT, vT, sT, extT, rT, UN, UT, UM):
	print "one key collection", mF, tip, tn, rF, oF, bT, envT, vT, sT, extT, rT, UN, UT, UM
	try:
		dirCmd = 'mkdir ' + logDirDict['logInfo']
		os.system(dirCmd)
		dirCmd = 'mkdir ' + logDirDict['mantisInfo']
		os.system(dirCmd)
		dirCmd = 'mkdir ' + logDirDict['renderInfo']
		os.system(dirCmd)
		dirCmd = 'mkdir ' + logDirDict['onvifInfo']
		os.system(dirCmd)
		# mantis
		if mF:
			cpMantisLogToRender(tn, tip, mantisLogDict['syslog'], logDirDict['mantisInfo'])
			cpMantisLogToRender(tn, tip, mantisLogDict['acosd.err'], logDirDict['mantisInfo'])
			cpMantisLogToRender(tn, tip, mantisLogDict['acosd.out'], logDirDict['mantisInfo'])
			print "collection mantis Info complete."
		else:
			print "Donot need collection mantis Info."
		# render
		if rF:
			colRenderLog(logDirDict['renderInfo'])
			print "collection render Info complete."
		else:
			print "Donot need collection render Info."
		# onvif
		if oF:
			colOnvifLog(logDirDict["onvifInfo"])
			print "collection onvif Info complete."
		else:
			print "Donot need collection onvif Info."
		# readme
		newReadme(bT, envT, vT, sT, extT, rT, UN, UT, UM)
		# tar and cleanup
		tarLogwithTime(logDirDict["logInfo"])
		dirCmd = 'rm -rf ' + logDirDict['logInfo']
		os.system(dirCmd)
		# 邮件发送 待补充
	except OSError:
		print "collection_oneKey information failed"
		dirCmd = 'rm -rf ' + logDirDict['logInfo']
		os.system(dirCmd)

def cpMantisLogToRender(tegraTotal, startIp, logName, logDir):
	try:
		ipRange = startIp.split('.')
		ipS = int(ipRange[3])
		ipTotal = int(tegraTotal)
		logFile = logDir + '/' + logName.split('/')[3]
		while ipTotal >= 1:
			ip = ipRange[0] + '.' + ipRange[1] + '.' + ipRange[2] + '.' + str(ipS)
			cmdStr = "scp nvidia@" + ip + ':' + logName + ' ' + logDir
			logFileN = logFile + '_' + ip
			cmdStr += "; mv " + logFile + ' ' + logFileN
			print cmdStr
			os.system(cmdStr)
			ipS += 1
			ipTotal -= 1
	except OSError:
		print "cpMantisLogToRender failed!", tegraTotal, startIp, logName, logDir

def tarLogwithTime(logDir):
	try:
		tarName = '~/Desktop/log_'
		tarName += datetime.datetime.now().strftime('%Y%m%d.%H:%M:%S')
		tarName += '.tar.gz'
		colCmd = "sudo tar -zcvf "
		colCmd += tarName + ' '
		colCmd += logDir
		print colCmd
		os.system(colCmd)
		print "tarLogwithTime success"
	except OSError:
		print "tarLogwithTime failed"

def colRenderLog(logDir):
	try:
		# /var/log/syslog* renderLogDict["syslog"]
		logCmd = "cp " + renderLogDict["syslog"] + ' ' + logDir
		os.system(logCmd)
		#  renderLogDict["AquetiDaemon"]
		logCmd = "sudo cp " + renderLogDict["web"] + ' ' + logDir
		os.system(logCmd)
		#  renderLogDict["mongodb"]
#		logCmd = "cp " + renderLogDict["mongodb"] + ' ' + logDir
#		os.system(logCmd)
		#  renderLogDict["model.json"]
		logCmd = "cp " + renderLogDict["model.json"] + ' ' + logDir
		os.system(logCmd)
	except OSError:
		print "colRenderLog failed!", logDir

def colOnvifLog(logDir):
	try:
		logCmd = "cp -rf " + onvifLogDict["runLog"] + ' ' + logDir
		os.system(logCmd)
		logCmd = "cp " + onvifLogDict["xmlCfg"] + ' ' + logDir
		os.system(logCmd)
	except OSError:
		print "colOnvifLog failed!", logDir

def newReadme(bT, envT, vT, sT, extT, rT, UN, UT, UM):
	try:
		readmeFile = logDirDict['logInfo'] + "/readme"
		readmeFile += datetime.datetime.now().strftime('%Y%m%d.%H:%M:%S') + ".txt"
		dirCmd = 'touch ' + readmeFile
		os.system(dirCmd)
		readmeStr = "【问题详细记录单】"
		echoCmd = "echo " + readmeStr + " > " + readmeFile
		os.system(echoCmd)
		readmeStr = "【记录时间】\n	" + datetime.datetime.now().strftime('%Y%m%d.%H:%M:%S')
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【问题发现人联系方式】\n	" + "姓名: " + UN + "\n	电话:　" + UT + "\n	邮箱: " + UM
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【简要描述】\n	" + bT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【详细描述】"
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【环境信息 (软硬件和配套操作系统信息)】\n	" + envT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【版本信息 (配套版本和被测软件的版本信息)】\n	" + vT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【重现步骤 (重现问题的详细步骤)】\n	" + sT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【预期测试结果】\n	" + extT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【实际测试结果】\n	" + rT
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
		readmeStr = "【相关日志】\n	详见附件"
		echoCmd = "echo \"" + readmeStr + "\" >> " + readmeFile
		os.system(echoCmd)
	except OSError:
		print "newReadme ", readmeFile, " failed"

#模型

def click_model_cfg():
	print "need add click_model_cfg logic"
	top = Toplevel()
	top.title("模型")
	# cfg MODLE ctrl
	# Model Configuration
	ModleCfgFrame = LabelFrame(top, text=' 模型配置 ', fg = 'green')
	ModleCfgFrame.grid(row=2, column=0, padx=10, pady=5)
	ModelFrame = LabelFrame(ModleCfgFrame, text =' 模型调整 ')
	ModelFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N)
	PathModelFrame = LabelFrame(ModelFrame, text = ' 模型路径 ' )
	PathModelFrame.grid(row=0, column=0, padx=10, pady=5)
	Label(PathModelFrame, text="模型文件 ", width=8).grid(row = 0, column = 0, padx=5, pady=5)
	global path
	path = StringVar();path.set(modelDict['DefModelPath'])
	Entry(PathModelFrame, textvariable = path, width=22).grid(row = 0, column = 1, padx=5, pady=5)
	Button(PathModelFrame, text ="路径选择", width=10, bg ='green', command = selectPath).grid(row = 0, column = 2, padx=5, pady=5)
	Label(PathModelFrame, text = "相机昵称 ", width=8).grid(row = 1, column = 0, padx=5, pady=5)
	defNickName = StringVar(); defNickName.set(modelDict['NickName']);
	NickName = Entry(PathModelFrame, textvariable=defNickName, width=22).grid(row=1, column=1, padx=5, pady=5)
	Button(PathModelFrame, text ="重置模型", width=10, bg ='green',\
		command=lambda:recovery_model(os.path.split(path.get())[0])).grid(row = 1, column = 2, padx=5, pady=5)
	#0: pagoda; 1: trapezoid; 2: panorama.
	FileModelFrame = LabelFrame(ModelFrame, text = ' 模型选择 ')
	FileModelFrame.grid(row=1, column=0, padx=10, pady=5, sticky=W)
	Label(FileModelFrame, text = "模型类别", width = 8).grid(row=0,column=0, padx=5, pady=5)
	defSaveAs = StringVar(); saveAs = ttk.Combobox(FileModelFrame, textvariable = defSaveAs, width = 21);
	saveAs["values"] = ['pagoda', 'panorama LH', 'panorama FH']; saveAs.current(0); 
	saveAs.grid(row=0, column = 1,padx=5, pady=5)
	Label(FileModelFrame, text = '时间戳', width = 8).grid(row = 1, column=0, padx=5, pady=5)
	defTimeS = StringVar(); TimeS = Entry(FileModelFrame, textvariable = defTimeS, width=22, state='readonly');
	defTimeS.set(update_max_timestamp(os.path.split(path.get())[0], modelDict['ModelEdit']));
	TimeS.grid(row=1, column=1, padx=5, pady=5)
	Button(FileModelFrame, text = '自定义 ', width = 10, height = 1, bg = 'green', \
			command=lambda:custom_model_cfg(os.path.split(path.get())[0], saveAs.get()))\
			.grid(row=0,column=2, padx=5, pady=5)
	Button(FileModelFrame, text = '触发', width=10, height=1, bg = 'green', \
			command=lambda:StartModelAdder(os.path.split(path.get())[0], defNickName.get(), saveAs.get()))\
			.grid(row=1, column=2, padx=5, pady=5)
	# hint MODLE ctrl
	HintModelFrame = LabelFrame(ModleCfgFrame, text = ' 校正 ')
	HintModelFrame.grid(row = 0, column = 1, padx = 7, pady = 5, sticky=N)
	Label(HintModelFrame, image=modleLogo).grid(row=0, column=0, padx = 8, pady = 5, columnspan=2)
	Button(HintModelFrame, text = '模型校正', width=15, height=1, bg = 'green', \
			command=lambda:StartModelEditor()).grid(row=1, column=0, padx=10, pady=5)
#实际上，该函数的分割并不智能，它仅仅是以 "PATH" 中最后一个 '/' 作为分隔符，分隔后，将索引为0的视为目录（路径），将索引为1的视为文件名

def selectPath():
	path_ = tkFileDialog.askopenfilename()             #获取文件路径
	path.set(path_)

def popSimpleDialog(level, hintStr):
	userStr = hintStr + "输入 [OK] 使之生效."
	rsp = tkSimpleDialog.askstring(level, userStr)
	print rsp
	if 'OK' != rsp:
		return False
	return True
#tkSimpleDialog.askinteger(title, prompt [,options])。要求用户输入一个字符串值。如果用户按下了Enter键或敲击了OK，那么函数返回这个字符串。如果用户通过按下Esc或敲击Cancel或显式地由窗口管理器关闭了这个对话框，则这个函数返回None。


def recovery_model(dirpath):
	try:
		if False == popSimpleDialog("NOTICE", simpleDialogDict['InitModel']):
			print "User cancel the action"
			return
		if not(os.path.isdir(dirpath)):                                           #os.path.isdir()用于判断对象是否为一个目录
			print (" Err: Invalid path dir " + dirpath)
			return
		recModel = dirpath + '/' + modelDict['ModelPagoda']
		print recModel
		if os.path.isfile(recModel):
			rmCmd = 'sudo rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['ModelPanoLH']
		if os.path.isfile(recModel):
			rmCmd = 'sudo rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['ModelPanoFH']
		if os.path.isfile(recModel):
			rmCmd = 'sudo rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['CustomModel']
		if os.path.isfile(recModel):
			rmCmd = 'sudo rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
	except OSError:
		print ("Delete user define modelFile failed.")
    	return


def custom_model_cfg(dirpath, saveAs):
	try:
		if not(os.path.isdir(dirpath)):
			print (" Err: Invalid path dir " + dirpath)
			return
		initModel = dirpath + '/' + modelDict['ModelEdit']
		customModel = dirpath + '/'
		if 'pagoda' == saveAs.strip():
			customModel += modelDict['ModelPagoda']
		elif 'panorama LH' == saveAs.strip():
			customModel +=  modelDict['ModelPanoLH']
		elif 'panorama FH' == saveAs.strip():
			customModel += modelDict['ModelPanoFH']
		else:
			customModel += modelDict['CustomModel']
		if not(os.path.isfile(customModel)):
			cpModel = 'cp ' +  initModel + ' ' + customModel
			os.system(cpModel)
		customCmd = "sudo geany " + customModel
		os.system(customCmd)
		key = 'timestamp'
		with open(customModel, "r") as f:
			for line in f:
				if key in line:
					print eval(line.split(':')[1].strip())
					defTimeS.set(eval(line.split(':')[1].strip()))
					break
	except OSError:
		print ("custom modelFile ", dirpath, " abnormal.")
    	return

def StartModelEditor():
	try:
		print ('Start ModelEditor base on Cur Model.')
		ModelEditorCmd = 'ModelEditor --hugin'
		os.system(ModelEditorCmd)
	except OSError:
		print ('Err: start ModelEditor tool failed, maybe reinstall the tool.')
		return

def StartModelAdder(dirpath, nickname, saveAs):
	try:
		if not(os.path.isdir(dirpath)):
			print (" Err: Invalid path dir " + dirpath)
			return
		modelFile = ""
		if 'pagoda' == saveAs.strip():
			modelFile = modelDict['ModelPagoda']
		elif 'panorama LH' == saveAs.strip():
			modelFile =  modelDict['ModelPanoLH']
		elif 'panorama FH' == saveAs.strip():
			modelFile = modelDict['ModelPanoFH']
		else:
			modelFile = modelDict['CustomModel']
		customModel = dirpath + '/' + modelFile
		print ('Select ModelFile: ' + customModel)
		defTimeS.set(update_max_timestamp(dirpath, modelFile));
		addertModelCmd = 'ModelAdder ' + nickname + ' ' + customModel
		print ('ModerAdder Cmd[' + addertModelCmd + ']')
		os.system(addertModelCmd)
	except OSError:
		print ('Err: start ModelAdder tool failed, please check nickname, maybe reinstall the tool.')
		return

def update_max_timestamp(dirpath, modelFile):
	CurFileName = dirpath + '/' + modelFile
	fileName = dirpath + '/' + modelDict['ModelEdit']
	key = 'timestamp'
	curTimeStamp = "0"
	maxTimeStamp = "0"
	if os.path.isfile(CurFileName):
		with open(CurFileName, "r") as f:
			for line in f:
				if key in line:
					curTimeStamp = eval(line.split(':')[1].strip())
					print "TimeStamp in", CurFileName, curTimeStamp
					break
	else:
		print "Invalid dir path or file name",  CurFileName
		return maxTimeStamp
	maxTimeStamp = curTimeStamp
	if os.path.isfile(fileName):
		fileData = ""
		with open(fileName, "r") as f:
			for line in f:
				if key in line:
					oldStr = eval(line.split(':')[1].strip())
					if int(oldStr) > int(curTimeStamp):
						curTimeStamp = oldStr
					maxTimeStamp = str(int(curTimeStamp) + 1)
					line = line.replace(oldStr, maxTimeStamp)
				fileData += line
		with open(fileName, "w") as f:
			f.write(fileData)
	fileData = ""
	with open(CurFileName, "r") as f:
		for line in f:
			if key in line:
				curTimeStamp = eval(line.split(':')[1].strip())
				line = line.replace(curTimeStamp, maxTimeStamp)
			fileData += line
	with open(CurFileName, "w") as f:
			f.write(fileData)
	return maxTimeStamp


#PTZ

def click_ptz_ctrl():
	print "need add click_ptz_ctrl logical"
	top = Toplevel()
	top.title("PTZ")
	# ptz ctrl 
	PtzFrame = LabelFrame(top, text = ' PTZ控制 ', fg = 'green')
	PtzFrame.grid(row=0, column=0, padx=10, pady=5, sticky=NW)
	Label(PtzFrame, text="移动速度", fg='green').grid(row=0, column=3, columnspan=2,padx=1,sticky=S)
	Label(PtzFrame, text="P").grid(row=1, column=3, padx=1)
	PS=StringVar();PS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=PS,orient=HORIZONTAL).grid(row=1, column=4, padx=1)
	Label(PtzFrame, text="T").grid(row=2, column=3, padx=1)
	TS=StringVar();TS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=TS,orient=HORIZONTAL).grid(row=2, column=4, padx=1)
	Label(PtzFrame, text="Z", width=2).grid(row=3, column=3, padx=1)
	ZS=StringVar();ZS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=ZS,orient=HORIZONTAL).grid(row=3, column=4, padx=1)
	Button(PtzFrame, width = 40, height = 40, image = PTZLeft, command=lambda:PTZMotion('Pan Left', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=1,column=0, padx=2, rowspan = 2)
	Button(PtzFrame, width = 40, height = 40, image = PTZRight, command=lambda:PTZMotion('Pan Right', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=1,column=2, padx=2, rowspan = 2)
	Button(PtzFrame, width = 40, height = 40, image = PTZUp, command=lambda:PTZMotion('Tilt Up', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=0,column=1, padx=2)
	Button(PtzFrame, width = 40, height = 40, image = PTZDown, command=lambda:PTZMotion('Tilt Down', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=3,column=1, padx=2)
	Button(PtzFrame, width = 50, height = 30, image = PTZIn, command=lambda:PTZMotion('Zoom In', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=1,column=1, padx=2)
	Button(PtzFrame, width = 50, height = 30, image = PTZOut, command=lambda:PTZMotion('Zoom Out', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=2,column=1, padx=2)
	Button(PtzFrame, width = 44, height = 44, image = PTZStop, command=lambda:PTZMotion('PTZ Stop', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=0, column=2,rowspan=2, sticky=N)
	Button(PtzFrame, width = 43, height = 43, image = PTZHome, command=lambda:PTZMotion('PTZ Home', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
		).grid(row=2, column=2,rowspan=2, sticky=S)
	# Home Set
	HomeFrame = LabelFrame(top, text=' 看守卫修正 ', fg='green'); HomeFrame.grid(row=0, column=1, padx=10, pady=5, sticky=NW)
	Label(HomeFrame, text="Pan\n坐标").grid(row=0, column=0,padx=2)
	Label(HomeFrame, text="Tilt\n坐标").grid(row=1, column=0,padx=2)
	Label(HomeFrame, text="Zoom\n坐标").grid(row=2, column=0,padx=2)
	HP=StringVar();HP.set(0.0);Scale(HomeFrame, from_=-90.0, to=90.0, resolution=0.1,variable=HP,orient=HORIZONTAL).grid(row=0, column=1, padx=2)
	HT=StringVar();HT.set(0.0);Scale(HomeFrame, from_=-50.0, to=50.0, resolution=0.1,variable=HT,orient=HORIZONTAL).grid(row=1, column=1, padx=2)
	HZ=StringVar();HZ.set(2.0);Scale(HomeFrame, from_=0.1, to=50.0, resolution=0.1,variable=HZ,orient=HORIZONTAL).grid(row=2, column=1, padx=2)
	Button(HomeFrame, width = 15, height=2, text = '设置看守卫\n(使用左侧指定的坐标)', bg = 'green',\
					command=lambda:SetHomePosition(IP.get(), OP.get(), 0, HP.get(), HT.get(), HZ.get())).grid(row=0, column=2, padx=7, pady=7,sticky=W)
	Button(HomeFrame, width = 15, height=2, text = '设置看守卫\n(使用图像当前位置)', bg = 'green',\
					command=lambda:SetHomePosition(IP.get(), OP.get(), 1, 0,0,0)).grid(row=1, column=2, padx=7, pady=7,sticky=W)
	Button(HomeFrame, width = 15, height=2, text = '重置看守卫\n默认值(0, 0, 2)', bg = 'green',\
					command=lambda:SetHomePosition(IP.get(), OP.get(), 2, 0,0,0)).grid(row=2, column=2, padx=7, pady=7,sticky=W)
	# onvif presetTour ctrl para
	TourCtrlFrame = LabelFrame(top, text=' 预置位巡航控制 ', fg = 'green')
	TourCtrlFrame.grid(row=1, column=0, padx=10, pady=5, sticky=W,columnspan=2)
	PresetFrame = LabelFrame(TourCtrlFrame, text = ' 预置位参数设置 ')
	PresetFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N, rowspan=2)
	Label(PresetFrame, text="预置位次序", width=10, height = 2, anchor = 'c').grid(row=0, column=0)
	Label(PresetFrame, text="驻留时间, 速度(P/T/Z)", width=15, height = 2, anchor = 'c').grid(row=0, column=1)
	Label(PresetFrame, text='预置位_01', width=10, height=1, anchor='c').grid(row=1, column=0, pady=0)
	preset1 = StringVar();preset1.set(ptzDict['tourDefault1']);Entry(PresetFrame, textvariable=preset1, width=14).grid(row=1, column=1)
	Label(PresetFrame, text='预置位_02', width=10, height=1, anchor='c').grid(row=2, column=0)
	preset2 = StringVar();preset2.set(ptzDict['tourDefault2']);Entry(PresetFrame, textvariable=preset2, width=14).grid(row=2, column=1)
	Label(PresetFrame, text='预置位_03', width=10, height=1, anchor='c').grid(row=3, column=0)
	preset3 = StringVar();preset3.set(ptzDict['tourDefault']);Entry(PresetFrame, textvariable=preset3, width=14).grid(row=3, column=1)
	Label(PresetFrame, text='预置位_04', width=10, height=1, anchor='c').grid(row=4, column=0)
	preset4 = StringVar();preset4.set(ptzDict['tourDefault']);Entry(PresetFrame, textvariable=preset4, width=14).grid(row=4, column=1)
	Label(PresetFrame, text='预置位_05', width=10, height=1, anchor='c').grid(row=5, column=0)
	preset5 = StringVar();preset5.set(ptzDict['tourDefault']);Entry(PresetFrame, textvariable=preset5, width=14).grid(row=5, column=1)
	Label(PresetFrame, text='预置位_06', width=10, height=1, anchor='c').grid(row=6, column=0)
	preset6 = StringVar();preset6.set(ptzDict['tourDefault']);Entry(PresetFrame, textvariable=preset6, width=14).grid(row=6, column=1)
	MoveFrame = LabelFrame(TourCtrlFrame, text = ' 持续运动 ')
	MoveFrame.grid(row=0, column=1, padx=5, pady=5, sticky=N, rowspan=2)
	moveFlag = IntVar(); Checkbutton(MoveFrame, text="运动",variable = moveFlag, width = 6).grid(row=0,column=1)
	Label(MoveFrame, text="方向", width=6, height = 2, anchor = 'e').grid(row=1, column=0)
	Label(MoveFrame, text="速度", width=6, height = 2, anchor = 'w').grid(row=1, column=1)
	index = 2
	for item in ['Pan', 'Tilt', 'Zoom']:
		Label(MoveFrame, text=item, width=5, height=2, anchor='e').grid(row=index, column=0)
		index += 1
	panSpeed = StringVar(); panSpeed.set(0);Entry(MoveFrame, textvariable=panSpeed, width=6).grid(row=2, column=1)
	tiltSpeed = StringVar(); tiltSpeed.set(1.2);Entry(MoveFrame, textvariable=tiltSpeed, width=6).grid(row=3, column=1)
	zoomSpeed = StringVar(); zoomSpeed.set(1.2);Entry(MoveFrame, textvariable=zoomSpeed, width=6).grid(row=4, column=1)

	TourFrame = LabelFrame(TourCtrlFrame, text=' 控制命令 ')
	TourFrame.grid(row=0, column=3, padx=5, pady=5, sticky=N)
	Button(TourFrame, text = '启动巡航', width = 10, height = 2, bg = 'green', \
			command=lambda:startTour(IP.get(), OP.get(), \
			preset1.get(), preset2.get(),preset3.get(),preset4.get(),preset5.get(), preset6.get(),\
			moveFlag.get(), panSpeed.get(), tiltSpeed.get(), zoomSpeed.get())).grid(row=0,column=0, padx=8, pady=5)
	Button(TourFrame, text = '停止巡航', width = 10, height = 2, bg = 'green', \
			command=lambda:stopTour(IP.get(), OP.get())).grid(row=0,column=1, padx=9, pady=5)

	SetPresetFrame = LabelFrame(TourCtrlFrame, text = ' 预置位配置 ')
	SetPresetFrame.grid(row=1, column=3, padx=5, pady=5, sticky=N)
	Label(SetPresetFrame, text="预置位名称", width=10, height = 1, anchor = 'e').grid(row=0,column=0, padx=5, pady=5, columnspan=3)
	presetList = StringVar();pList = ttk.Combobox(SetPresetFrame, textvariable=presetList, width=16);
	pList["values"] = ['Preset_01', 'Preset_02', 'Preset_03', 'Preset_04', 'Preset_05', 'Preset_06', 'custom'];
	pList.current(0); pList.grid(row=0,column=3, padx=5, pady=5, columnspan=3)
	Button(SetPresetFrame, text = '设置', width = 6, height=1,bg='green',\
			command=lambda:PresetConfigure(pList.get(), 'SET', IP.get(), OP.get())).grid(row=1,column=0,padx=4,pady=5, columnspan=2)
	Button(SetPresetFrame, text = '删除', width = 6, height=1,bg='green',\
			command=lambda:PresetConfigure(pList.get(), 'DEL', IP.get(), OP.get())).grid(row=1,column=2,padx=4,pady=5, columnspan=2)
	Button(SetPresetFrame, text = '运动到', width = 6, height=1,bg='green',\
			command=lambda:PresetConfigure(pList.get(), 'GOTO', IP.get(), OP.get())).grid(row=1,column=4,padx=4,pady=5, columnspan=2)

def PTZMotion(cmd, ps, ts, zs, ip, op):
	try:
		panSpeed = 0
		tiltSpeed = 0
		zoomSpeed = 0
		if 'Pan Left' == cmd.strip():
			panSpeed = -1 * float(ps) / 100
		elif 'Pan Right' == cmd.strip():
			panSpeed = float(ps) / 100
		elif 'Tilt Up' == cmd.strip():
			tiltSpeed = float(ts) / 100
		elif 'Tilt Down' == cmd.strip():
			tiltSpeed = -1 * float(ts) / 100
		elif 'Zoom In' == cmd.strip():
			zoomSpeed = float(zs) / 100
		elif 'Zoom Out' == cmd.strip():
			zoomSpeed = -1 * float(zs) / 100
		print cmd, panSpeed, tiltSpeed, zoomSpeed
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'PTZMotion Connect', ip, op, 'success!'
		cmdStr = 'PTZ '
		if 'PTZ Home' == cmd.strip():
			cmdStr += 'GOTO HOME '
		else:
			cmdStr += 'Continue Motion '
		cmdStr += '['+ str(panSpeed) + ' ' + str(tiltSpeed) + ' ' + str(zoomSpeed) + ']\r\n'
		print cmdStr
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()

def SetHomePosition(ip, op, flag, pp, tp, zp):
	try:
		print ip, op, flag, pp, tp, zp
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'SetHomePosition Connect', ip, op, 'success!'
		cmdStr = 'Set Home Position '
		if 0 == flag:
			cmdStr += 'Specify [' + str(pp) + ' ' + str(tp) + ' ' + str(zp) + ']'
		elif 1 == flag:
			cmdStr += 'Current'
		elif 2 == flag:
			cmdStr += 'Reset'
		print cmdStr
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		clientSock.close()
	except socket.error, e:
		print "Set Home Position on", ip, op, "failed"
		print e, int(op)
		traceback.print_exec()

def startTour(ip, op, p1, p2, p3, p4, p5, p6, mf, ps, ts, zs):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'startTour Connect', ip, op, 'success!'
		cmdStr = 'Tour '
		for item in [p1, p2, p3, p4, p5, p6]:
			cmdStr += item.replace(' ', '') + ';'
		if mf:
			cmdStr += '--- 1 '
			cmdStr += ps + ' ' + ts + ' ' + zs
		cmdStr += '\r\n'
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		''' rsp
		ret = str(clientSock.recv(1024))
		print ret
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()
		#sys.exit(1)

def stopTour(ip, op):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'stopTour Connect', ip, op, 'success!'
		cmdStr = 'Tour stop preset tour\r\n';
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		'''
		wait rsp
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()


def PresetConfigure(name, cmd, ip, op):
	try:
		print 'cmd para:', name, cmd, ip, op
		clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'preset configure connect success'
		cmdStr = 'PTZ PRESET ' + cmd + ' ' + name + '\r\n';
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		clientSock.close()
	except socket.error, e:
		print "connect", ip, op, "failed.", e
		traceback.print_exc()

def reInstall_onvif(time):
	if '0' != time:
		if False == popSimpleDialog("NOTICE", simpleDialogDict['ReinstallOnvif']):
			print "User cancel the action"
			return
	print os.system("pwd");
	rebuild_commad = 'sudo dpkg -r mantis_onvifserver;'
#	rebuild_commad += 'make ONVIFServer;'
	rebuild_commad += 'sudo dpkg -i ./mantis_ONVIFServer-*_.deb'
	
	# start onvifServer
	if os.system(rebuild_commad) == 0:
		print 'Successful ReInstall onvifServer on', rebuild_commad
	else:
		print 'ReInstall onvifServer Completed'
		

	
xmenu = Menu(root)
#创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方

maintainMenu = Menu(xmenu, tearoff = 0)
#定义一个空菜单单元 tearoff=1时，悬浮菜单
xmenu.add_cascade(label = '维护', menu = maintainMenu)
#将上面定义的空菜单命名为`维护`，放在菜单栏中，就是装入那个容器中
maintainMenu.add_command(label = '检查网络连接',command =click_check_network)
#在`维护`中加入`检查网络连接`的小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。如果点击这些单元, 就会触发对应功能
maintainMenu.add_command(label = '检查机头服务', command = click_maintain)
maintainMenu.add_command(label = '查询录像列表', command = click_queryClip)
maintainMenu.add_command(label = '故障信息收集', command = infomation_col)

advancedMenu = Menu(xmenu, tearoff = 0)
xmenu.add_cascade(label = '高级', menu = advancedMenu)
advancedMenu.add_command(label = 'PTZ控制', command = click_ptz_ctrl)
advancedMenu.add_command(label = '模型配置', command = click_model_cfg)

helpMenu = Menu(xmenu, tearoff = 0)
xmenu.add_cascade(label = '帮助', menu = helpMenu)
helpMenu.add_command(label = '用户指南', command = click_help_onvif)
helpMenu.add_command(label = '关于', command = click_about_me)

xmenu.add_command(label = '退出', command = quit_window)


ParaFrame = LabelFrame(root, text='ONVIF控制',  fg = 'green')
ParaFrame.grid(row=0, column=0, padx=10, pady=10)
#LabelFrame(master, **options)  master -- 父组件  **options -- 组件选项  用于窗口布局的容器  grid网格大小位置


#onvif start para
OnvifFrame = LabelFrame(ParaFrame, text=' 启动参数 ')
OnvifFrame.grid(row=0, column=0, padx=10, pady=10, rowspan = 5, sticky=N) 
onvifParaIndex = 1
for item in ['服 务 器 地 址: ', 'Rtsp  端 口 号: ', 'Onvif  端 口 号: ', '编  码   类  别: ', '分辨率 (H*W): ', '图  像   质  量: ',  '服  务   器  ID: ','相  机   昵  称: ']:
	Label(OnvifFrame, text=item, width = 13, height = 2, anchor='e').grid(row=onvifParaIndex,column=0,padx=0)
	onvifParaIndex += 1
#Label标签控件；可以显示文本和位图

#Entry文本  StringVar是可变字符串，get()和set()是得到和设置其内容
defRIP = StringVar(); defRIP.set(get_host_ip()); IP = Entry(OnvifFrame, textvariable = defRIP, width=23); IP.grid(row=1,column=1, padx=10, columnspan=2)
defRP = StringVar(); defRP.set(onvifDict['rtspPort']); RP = Entry(OnvifFrame, textvariable = defRP, width=23); RP.grid(row=2,column=1, columnspan=2)
defOP = StringVar(); defOP.set(onvifDict['onvifPort']); OP = Entry(OnvifFrame, textvariable = defOP, width=23); OP.grid(row=3,column=1, columnspan=2)

#Combobox下拉框
defEnc = StringVar(); encType = ttk.Combobox(OnvifFrame, textvariable=defEnc, width=21);
encType["values"] = ['h264', 'JPEG', 'h265']; encType.current(onvifDict['EncDef']); encType.grid(row=4,column=1, columnspan=2)
defRes = StringVar(); resDefine = ttk.Combobox(OnvifFrame, textvariable=defRes, width=21);
resDefine["values"] = [ onvifDict['HW4K'], onvifDict['HW1080P'],onvifDict['HWCustom']]; resDefine.current(onvifDict['ResDef']); resDefine.grid(row=5,column=1, columnspan=2);

#文本
defImgQ = StringVar(); defImgQ.set(onvifDict['imgQuality']);imgQ = Entry(OnvifFrame, textvariable = defImgQ, width=23); imgQ.grid(row=6,column=1, columnspan=2)
defRender = StringVar(); defRender.set(getRenderServerID(daemonDict['configuration'])); Render = Entry(OnvifFrame, textvariable = defRender, width=23); Render.grid(row=7, column=1, columnspan=2)
defNName = StringVar(); defNName.set(modelDict['NickName']);  NName = Entry(OnvifFrame, textvariable = defNName, width=23); NName.grid(row=8,column=1, columnspan=2)

# 复选框Checkbutton；grid网格设置sticky=N/S/E/W:顶端对齐/底端对齐/右对齐/左对齐
CB = IntVar(); CB.set(onvifDict['RootDef']);Checkbutton(OnvifFrame, height = 2, text="超级权限",variable = CB).grid(row=9,column=0, sticky=E)
defRecord = IntVar(); defRecord.set(onvifDict['RecordDef']);Checkbutton(OnvifFrame, height = 2, text = "启动时启动录像", variable = defRecord).grid(row=9, column=2, sticky=W)
Crop = IntVar(); Crop.set(onvifDict['CropDef']);Checkbutton(OnvifFrame, height = 2, text = "裁剪", variable = Crop).grid(row=9, column=1)

# button ctrl onvif
StartFrame = LabelFrame(ParaFrame, text=' 控制命令 ')
StartFrame.grid(row=0, column=1, padx=10, pady=5, sticky=N)
Label(StartFrame, image=onvifLogo).grid(row=0, column=0, columnspan=3)
Button(StartFrame, text = '启动ONVIF', width = 8, height = 2, borderwidth=2, bg = 'green',command=lambda:click_start_onvif(CB.get(), IP.get(), RP.get(), OP.get(), encType.get(), resDefine.get(), Render.get(), NName.get(), defRecord.get(), imgQ.get(), Crop.get())).grid(row=1,column=0, padx=2, pady=5)
Button(StartFrame, text = '启动录像', width = 8, height = 2, bg = 'green', command=lambda:CtrlRecord(IP.get(), OP.get(), 'start')).grid(row=1,column=1, padx=2, pady=5)
Button(StartFrame, text = '停止录像', width = 8, height = 2, bg = 'green', command=lambda:CtrlRecord(IP.get(), OP.get(), 'stop')).grid(row=1,column=2, padx=2, pady=5)

# cfg 
CfgFrame = LabelFrame(ParaFrame, text=' 更新配置 ')
CfgFrame.grid(row=1, column=1, padx=10, pady=5, sticky=N)
Button(CfgFrame, text = '恢复出厂设置', width = 12, height = 2, borderwidth=2, bg = 'green', command=lambda:restoreCfg()).grid(row=10,column=0, padx=10, pady = 5)
Button(CfgFrame, text = '保存作为默认', width = 12, height = 2, bg = 'green',command=lambda:saveAsDefultCfg(CB.get(), IP.get(), RP.get(), OP.get(), encType.get(), resDefine.get(),Render.get(), NName.get(), defRecord.get(), imgQ.get(), Crop.get())).grid(row=10,column=1,padx=10, pady=5)

# vlc live
liveFrame = LabelFrame(ParaFrame, text = ' 视频预览 ')
liveFrame.grid(row=2, column=1, padx=10, pady=5, sticky=SW)
Label(liveFrame, text='视频传输方式  ', width=13, height=1, anchor='e').grid(row=0, column=0, padx=0,pady=5)
defTransport = StringVar();Transport=ttk.Combobox(liveFrame, textvariable=defTransport, width=13);
Transport["values"]=['TCP', 'UDP'];Transport.current(1);Transport.grid(row=0, column=1, padx=2,pady=5)
Button(liveFrame, image = VideoPlay, width = 41, height = 30, borderwidth=1, bg = 'green',command=lambda:vlcPlay(IP.get(), RP.get(), Transport.get())).grid(row=0, column=2,padx=5,pady=5)



#28181 Ctrl
Gb28181Frame = LabelFrame(root, text=' GB28181 控制 ', fg = 'green')
Gb28181Frame.grid(row=1, column=0, padx=10, pady=10)
GbFrame = LabelFrame(Gb28181Frame, text=' 启动参数 ')
GbFrame.grid(row=0, column=0, padx=10, pady=10, rowspan = 5, sticky=N)

# check and  create gb cfg file
check_and_create_file(gbDict['gbCfgFileDir'], gbDict['gbCfgFileName'])
# gb para
for index in range(len(gbCfgListChinese)):
	 Label(GbFrame, text=gbCfgListChinese[index] + '  ',width = 13, height = 2, anchor='c').grid(row=index,column=0,padx=0)
	 

defgbSid = StringVar(); defgbSid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_id')); gbSid = Entry(GbFrame, textvariable = defgbSid, width=23); gbSid.grid(row=0, column=1, padx=10)
defgbSip = StringVar(); defgbSip.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_ip')); gbSip = Entry(GbFrame, textvariable = defgbSip, width=23); gbSip.grid(row=1,column=1)
defgbSpo = StringVar(); defgbSpo.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_port')); gbSpo = Entry(GbFrame, textvariable = defgbSpo, width=23); gbSpo.grid(row=2,column=1)
defgbDid = StringVar(); defgbDid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'device_id')); gbDid = Entry(GbFrame, textvariable = defgbDid, width=23); gbDid.grid(row=3,column=1)
defgbLpo = StringVar(); defgbLpo.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'listen_port')); gbLpo = Entry(GbFrame, textvariable = defgbLpo, width=23); gbLpo.grid(row=4,column=1)
defgbUsername = StringVar(); defgbUsername.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'username')); gbUsername = Entry(GbFrame, textvariable = defgbUsername, width=23); gbUsername.grid(row=5,column=1)
defgbPwd = StringVar(); defgbPwd.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'password')); gbPwd = Entry(GbFrame, textvariable = defgbPwd, width=23, show='*'); gbPwd.grid(row=6,column=1)
defgbCam = StringVar(); defgbCam.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'cameral_system')); gbCam = Entry(GbFrame, textvariable = defgbCam, width=23); gbCam.grid(row=7,column=1)
defgbAid = StringVar(); defgbAid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'alarm_id')); gbAid = Entry(GbFrame, textvariable = defgbAid, width=23); gbAid.grid(row=8,column=1)
defgbMid = StringVar(); defgbMid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'media_id')); gbMid = Entry(GbFrame, textvariable = defgbMid, width=23); gbMid.grid(row=9,column=1)
defgbRex = StringVar(); defgbRex.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'register_expire')); gbRex = Entry(GbFrame, textvariable = defgbRex, width=23); gbRex.grid(row=10,column=1)

# button ctrl 28181
Ctrl28181Frame = LabelFrame(Gb28181Frame, text=' 控制&配置 ')
Ctrl28181Frame.grid(row=0, column=1, padx=10, pady=5, sticky=N)
gbLogo = PhotoImage(file=gbDict['gbLogoFile'])
Label(Ctrl28181Frame, image=gbLogo).grid(row=1, column=0, columnspan=2)
Button(Ctrl28181Frame, text = '启动  GB28181', width = 12, height = 2, bg = 'green', command=lambda:click_start_gb()).grid(row=2,column=0, padx=2, pady=5)
Button(Ctrl28181Frame, text = '更新  GB28181  配置信息', width = 15, height = 2, bg = 'green', command=lambda:update_gb_cfg()).grid(row=2,column=1, padx=2, pady=5)

liveFramegb = LabelFrame(Gb28181Frame, text = ' 视频预览 ')
liveFramegb.grid(row=1, column=1, padx=10, pady=5, sticky=NW)
Label(liveFramegb, text='视频流端口：', width = 13, height = 2, anchor='c').grid(row=0,column=0,padx=0)
defgbport = StringVar(); defgbport.set('6000');gbport = Entry(liveFramegb, textvariable = defgbport, width=13); gbport.grid(row=0,column=1,padx=2,pady=5)
Button(liveFramegb, image = VideoPlay, width = 41, height = 30, borderwidth=1, bg = 'green',command=lambda:vlcPlaygb()).grid(row=0, column=2,padx=2,pady=5)

#auto run
reInstall_onvif('0')
#click_start_onvif(CB.get(), IP.get(), RP.get(), OP.get(), encType.get(), resDefine.get(), \
#		Render.get(), NName.get(), defRecord.get(), imgQ.get(), Crop.get())


root['menu'] = xmenu
#将root的menu属性设置为xmenu
root.mainloop()
#显示，令根空间进入主循环，开始监听事件和执行相应的人机交互命令
