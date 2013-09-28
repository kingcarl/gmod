import DNS
import re
import types
from logger import elogger
                    
class Sensor:
    def __init__(self):
        DNS.DiscoverNameServers()
 
    def resolve(self, domain):
	try:
	    dns = DNS.Request(name=domain, qtype='A')
	    res = dns.req().answers
            return res
	except:
	    return False
    
    def result_parse(self, answers, rights):
	err = []
	
	if answers:
	    for ans in answers: 
	        if ans['data'] not in rights:
		    err.append(ans['data'])
            return err
	else:
	    return ['resolver timeout']
    
    def ns_probe(self, bucket):
	err_domain = []
        for domain in bucket:
            hijack = self.result_parse(self.resolve(domain), bucket[domain])
            if hijack:
		err_domain.append("%s:(%s not in right rr list)" % (domain, ' , '.join(hijack)))
        return err_domain
