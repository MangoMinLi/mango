#! /usr/bin/env python
#-*- coding: UTF-8 -*-

from socket import *
import re                 #Regular Expression 正则表达式
import random
import time
import sys
from select import *
import threading
from random import randrange
import errno

# SIP request template
req_templ = \
"""$METHOD $TARGET_URI SIP/2.0\r
Via: SIP/2.0/UDP $LOCAL_IP:$LOCAL_PORT;rport;branch=z9hG4bK$BRANCH\r
Max-Forwards: 70\r
From: <sip:caller@pjsip.org>$FROM_TAG\r
To: <$TARGET_URI>$TO_TAG\r
Contact: <sip:$LOCAL_IP:$LOCAL_PORT;transport=udp>\r
Call-ID: $CALL_ID@pjsip.org\r
CSeq: $CSEQ $METHOD\r
Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, REFER\r
Supported: replaces, 100rel, norefersub\r
User-Agent: pjsip.org Python tester\r
Content-Length: $CONTENT_LENGTH\r
$SIP_HEADERS"""

def is_request(msg):
	return msg.split(" ", 1)[0] != "SIP/2.0"
	
def is_response(msg):
	return msg.split(" ", 1)[0] == "SIP/2.0"

def get_code(msg):
	if msg=="":
		return 0
	return int(msg.split(" ", 2)[1])

def get_tag(msg, hdr="To"):
	pat = "^" + hdr + ":.*"
	result = re.search(pat, msg, re.M | re.I)
	if result==None:
		return ""
	line = result.group()
	#print "line=", line
	tags = line.split(";tag=")
	if len(tags)>1:
		return tags[1]
	return ""
	#return re.split("[;& ]", s)

def get_header(msg, hname):
	headers = msg.splitlines()
	for hdr in headers:
		hfields = hdr.split(": ", 2)
		if hfields[0]==hname:
			return hfields[1]
	return None

class Dialog:
	sock = None
	dst_addr = ""
	dst_port = 5070
	local_ip = ""
	local_port = 5075
	tcp = False
#	call_id = str(random.random())
	cseq = 0
	local_tag = ";tag=" + str(random.random())
	rem_tag = ""
	last_resp_code = 0
	inv_branch = ""
	trace_enabled = True
	last_request = ""
	def __init__(self, dst_addr, dst_port=5070, tcp=False, trace=True, local_port=5075):
		self.dst_addr = dst_addr
		self.dst_port = dst_port
		self.tcp = tcp
		self.trace_enabled = trace
		if tcp==True:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.connect(dst_addr, dst_port)
		else:
			self.sock = socket(AF_INET, SOCK_DGRAM)
			self.sock.bind(("10.69.2.60", local_port))
		
		self.local_ip, self.local_port = self.sock.getsockname()
		self.trace("Dialog socket bound to " + self.local_ip + ":" + str(self.local_port))

	def trace(self, txt):
		if self.trace_enabled:
			print str(time.strftime("%H:%M:%S ")) + txt

	def update_fields(self, msg):
		if self.tcp:
			transport_param = ";transport=tcp"
		else:
			transport_param = ""
		msg = msg.replace("$TARGET_URI", "sip:"+self.dst_addr+":"+str(self.dst_port) + transport_param)
		msg = msg.replace("$LOCAL_IP", self.local_ip)
		msg = msg.replace("$LOCAL_PORT", str(self.local_port))
		msg = msg.replace("$FROM_TAG", self.local_tag)
		msg = msg.replace("$TO_TAG", self.rem_tag)
#		msg = msg.replace("$CALL_ID", self.call_id)
		msg = msg.replace("$CSEQ", str(self.cseq))
		branch=str(random.random())
		msg = msg.replace("$BRANCH", branch)
		return msg

	def create_req(self, method, sdp, branch="", extra_headers="", body=""):
		if branch=="":
			self.cseq = self.cseq + 1
		msg = req_templ
		msg = msg.replace("$METHOD", method)
		msg = msg.replace("$SIP_HEADERS", extra_headers)
		if branch=="":
			branch=str(random.random())
		msg = msg.replace("$BRANCH", branch)
		if sdp!="":
			msg = msg.replace("$CONTENT_LENGTH", str(len(sdp)))
			msg = msg + "Content-Type: application/sdp\r\n"
			msg = msg + "\r\n"
			msg = msg + sdp
		elif body!="":
			msg = msg.replace("$CONTENT_LENGTH", str(len(body)))
			msg = msg + "\r\n"
			msg = msg + body
		else:
			msg = msg.replace("$CONTENT_LENGTH", "0")
			msg = msg + "\r"
		return self.update_fields(msg)

	def create_response(self, request, code, reason, to_tag=""):
		response = "SIP/2.0 " + str(code) + " " + reason + "\r\n"
		lines = request.splitlines()
		for line in lines:
			hdr = line.split(":", 1)[0]
			if hdr in ["Via", "From", "To", "CSeq", "Call-ID"]:
				if hdr=="To" and to_tag!="":
					line = line + ";tag=" + to_tag
				elif hdr=="Via":
					line = line + ";received=127.0.0.1"
				response = response + line + "\r\n"
		return response

	def create_invite(self, sdp, extra_headers="", body=""):
		self.inv_branch = str(random.random())
		return self.create_req("INVITE", sdp, branch=self.inv_branch, extra_headers=extra_headers, body=body)

	def create_ack(self, sdp="", extra_headers=""):
		return self.create_req("ACK", sdp, extra_headers=extra_headers, branch=self.inv_branch)

	def create_bye(self, extra_headers=""):
		return self.create_req("BYE", "", extra_headers)

	def send_msg(self, msg, dst_addr=None):
		if (is_request(msg)):
			self.last_request = msg.split(" ", 1)[0]
		if not dst_addr:
			dst_addr = (self.dst_addr, self.dst_port)
		self.trace("============== TX MSG to " + str(dst_addr) + " ============= \n" + msg)
		self.sock.sendto(msg, 0, dst_addr)

	def wait_msg_from(self, timeout):
		endtime = time.time() + timeout
		msg = ""
		src_addr = None
		while time.time() < endtime:
			readset = select([self.sock], [], [], 1)
			if len(readset[0]) < 1 or not self.sock in readset[0]:
				if len(readset[0]) < 1:
					print "select() timeout (will wait for " + str(int(endtime - time.time())) + "more secs)"
				elif not self.sock in readset[0]:
					print "select() alien socket"
				else:
					print "select other error"
				continue
			try:
				msg, src_addr = self.sock.recvfrom(4096)
				break
			except:
				print "recv() exception: ", sys.exc_info()[0]
				continue

		if msg=="":
			return "", None
		if self.last_request=="INVITE" and self.rem_tag=="":
			self.rem_tag = get_tag(msg, "To")
			self.rem_tag = self.rem_tag.rstrip("\r\n;")
			if self.rem_tag != "":
				self.rem_tag = ";tag=" + self.rem_tag
			self.trace("=== rem_tag:" + self.rem_tag)
		self.trace("=========== RX MSG from " + str(src_addr) +  " ===========\n" + msg)
		return (msg, src_addr)
	
	def wait_msg(self, timeout):
		return self.wait_msg_from(timeout)[0]
		
	# Send request and wait for final response
	def send_request_wait(self, msg, timeout):
		t1 = 1.0
		endtime = time.time() + timeout
		resp = ""
		code = 0
		for i in range(0,2):
			self.send_msg(msg)
			resp = self.wait_msg(t1)
			if resp!="" and is_response(resp):
				code = get_code(resp)
				break
		last_resp = resp
		while code < 200 and time.time() < endtime:
			resp = self.wait_msg(endtime - time.time())
			if resp != "" and is_response(resp):
				code = get_code(resp)
				last_resp = resp
			elif resp=="":
				break
		return last_resp


def invite(dia,call_id):
	sdp=\
"""v=0\r
o=34020000001320000001 0 0 IN IP4 10.69.2.60\r
s=Play\r
c=IN IP4 10.0.12.144\r
t=0 0\r
m=video 6000 RTP/AVP 96 98 97\r
a=recvonly\r
a=rtpmap:96 PS/90000\r
a=rtpmap:98 H264/90000\r
a=rtpmap:97 MPEG4/90000\r
y=0100000001\r
f=\r"""
	msg=dia.create_invite(sdp)
	msgupdate = msg.replace("$CALL_ID", call_id)
	resp = dia.send_request_wait(msgupdate, 10)
	if resp=="":
		print "Can't waiti for response, Stop request"
		sys.exit(0)
	code = get_code(resp)
	if code==200:
		msgack=dia.create_ack()
		msgackupdate = msgack.replace("$CALL_ID", call_id)
		dia.send_msg(msgackupdate)
	else:
		msgerro = dia.create_req("CANCEL", sdp)
		msgerroupdate= msgerro.replace("$CALL_ID", call_id)
		dia.send_request_wait(msgerroupdate, 5)
		msgack = dia.create_ack()
		msgackupdate = msgack.replace("$CALL_ID", call_id)
		dia.send_msg(msgackupdate)
		sys.exit(0)

def bye(dia,call_id):
	msgbye = dia.create_bye()
	msgbyeupdate = msgbye.replace("$CALL_ID", call_id)
	respnew = dia.send_request_wait(msgbyeupdate, 1)
	codenew = get_code(respnew)
	if codenew==481:
		print "errorrrrrrrrr"
		endtimee=time.asctime(time.localtime(time.time()))
		print "开始时间：",timee
		print "结束时间：",endtimee
		sys.exit(0)

def run():
	call_id = str(random.random())
	dia=Dialog(dst_addr="10.69.2.60")
	print "invite"
	invite(dia,call_id)
	time.sleep(30)
	print "bye"
	bye(dia,call_id)
	t = threading.Timer(30, run)
	t.start()

if __name__=="__main__":
#	timerd=randrange(1,31,5)
#	print timerd
	global timee
	timee=time.asctime(time.localtime(time.time()))
	t = threading.Timer(30, run)
	t.start()






