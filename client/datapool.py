import wsender
import ConfigParser
import os
import sys
import re
from logger import elogger
from config import LOCATION, EMAIL_SERVER

class GetContent:
    def __init__(self):
        self.cp = ConfigParser.ConfigParser()
	try:
	    self.cp.read('./conf/seon.conf')
	except:
	    print "Can't open ./conf/seon.conf !"
	    sys.exit(1)
        
    def getconfig(self):
        secs = self.cp.sections()
	domainlist = []
        for sec in secs:
	    RR = self.cp.get(sec, 'RR')
            domainlist.append("%s:%s" % (sec, RR))
        return domainlist

class PutDataInPool:
    def __init__(self):
        self.pool = {}
        
    def get(self, host):
        return self.pool[host]
        
    def put(self, host, info):
        self.pool[host] = info
        
    def combine(self):
	txt = []
	ws = wsender.WarnSender(EMAIL_SERVER, 25)
        for host in self.pool.keys():
	    seg = self.get(host).split(':')
	    if seg[0]:
		if seg[1].find('normal') < 0:
            		txt.append("%s %s >> [ %s ]" % (seg[0], LOCATION[seg[0]], seg[2]))
	    
	if txt :
	    ws.send_email("<br>".join(txt))
	else:
	    ws.smtp.quit()


