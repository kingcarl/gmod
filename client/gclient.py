#!/usr/bin/env python
#Date:2013/2/8
#Author:Carl Guan

import socket
import sys
import ConfigParser
import time
import errno
import optparse
import select
from datapool import *
from warnings import *
from logger import elogger
from config import LOCATION

class AsyncClient:
    def __init__(self, sgroup, pool):
	self.datapool = pool
	self.group = sgroup
    
    def to_server_msgs(self):
	cont = GetContent()
	domainlist = cont.getconfig()
	
	return '&'.join(domainlist)
    
    def remove_none(self, sock_list):
	list = []
	for sock in sock_list:
	    if sock != None:
		list.append(sock)
	
	return list
    
    def async_connect(self):
	"""Connect to the given server and return a non-blocking socket."""
	
	def connect(group):		
	    socket.setdefaulttimeout(60)
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	    try:
	        elogger.INFO("%s:%s" % (group[0], group[1]))
	        sock.connect(group)
	        elogger.INFO("Connect to %s:%s successed !" % (group[0], group[1]))
	        sock.setblocking(0)
		
		return sock
	    except:
	        elogger.INFO("Connect to %s:%s failed !" % (group[0], group[1]))
		sock.close()
	    	    
    	return map(connect, self.group)
    
    def async_loop(self):
	msgs = self.to_server_msgs()
	sockets = self.remove_none(self.async_connect())
	
	num = len(msgs)
	msgs = "%d!" % num + msgs
	
	for sock in sockets:
	    sock.sendall(msgs)
	
	while sockets:
            rlist, _, _ = select.select(sockets, [], [])

	    for sock in rlist:
		data = ''
		
		while True:
		    try:
			new_data = sock.recv(4096)
		    except socket.error, e:
			if e.args[0] == errno.EWOULDBLOCK:
			    break
			raise
		    else:
			if not new_data:
			    break
			else:
			    data += new_data
		sockets.remove(sock)
		sock.close()
		self.datapool.put(sock, data)
		elogger.INFO("get msg %s" % data)
		
	self.datapool.combine()
 
def parse_args(addresses):
    usage = """usage: %prog [port]
    
This is the get resolve information client, asynchronous edition.
Run it like this:
 
  python client.py port
  
to grab dig information from servers on ports which you order.

Of course, there need to be servers listening on this port
for that to work.
"""
    parser = optparse.OptionParser(usage)
    _, port = parser.parse_args()
    if not port[0]:
	print parser.format_help()
	parser.exit()
	
    def parse_address(addr):
	if not port[0].isdigit():
	    parser.error('Ports must be integers.')
	return addr, int(port[0])
    
    return map(parse_address, addresses)

def main():
    datapool = PutDataInPool()
    group = parse_args(LOCATION.keys())
    ac = AsyncClient(group, datapool)
    ac.async_loop()
    
if __name__ == '__main__':
    main()

