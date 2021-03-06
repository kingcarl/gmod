import socket
import sys
import re
import time
from dns_sensor import *
from logger import elogger

class Sender: 
    def __init__(self, port):
        self.sor = Sensor()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(1)
    
    def create_bucket(self, msgs):
	bucket = {}
	headers = msgs.split('&')
	for h in headers:
	    info = h.split(':')
	    bucket[info[0]] = info[1]
	    
	return bucket
    
    def sr_loop(self):
        while True:
            sc, sockname = self.sock.accept()
            while True:          
		elogger.INFO("sock connects %s and %s" % (sc.getsockname(), sc.getpeername()))
		
		msgs = sc.recv(8196)
		data = msgs.split('!')
			
		if data[1] and len(data[1]) >= int(data[0]):
		    elogger.INFO("received %s" % data[1])
		    err_result = self.sor.ns_probe(self.create_bucket(data[1]))
		else:
		    elogger.INFO("received %s" % data[1])
		    elogger.INFO("packet less than header num and request loss string")
		    loss = int(data[0]) - len(data[1])
		    elogger.INFO("Loss:%d" % loss)
		    sc.sendall("Loss:%d" % loss)
		    time.sleep(0.5)
		    lmsgs = sc.recv(8196)
		    if lmsgs:
			elogger.INFO("receive loss string %s" % lmsgs)
			data[1] = data[1] + lmsgs
			err_result = self.sor.ns_probe(self.create_bucket(data[1]))
		    else:
			break
		
                if err_result:
		    elogger.INFO("send err result")
		    sc.sendall("%s: %s" % (sc.getsockname()[0], ','.join(err_result)))
		    elogger.INFO("%s: %s" % (sc.getsockname()[0], ','.join(err_result)))
                    break
                else:
		    sc.sendall("%s: normal" % sc.getsockname()[0])
		    elogger.INFO("domain check normal")
                    break
