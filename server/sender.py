import socket
import sys
import re
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
		
		msgs = sc.recv(4096)
		
		if msgs:
		    elogger.INFO("received %s" % msgs)
		    err_result = self.sor.ns_probe(self.create_bucket(msgs))
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

