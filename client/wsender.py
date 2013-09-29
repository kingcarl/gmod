#coding:gb2312
import subprocess
import smtplib
from config import EMAIL_ADDRS, PHONES, SUBJECT, FROMADDR, SMS_SERVER
from email.mime.text import MIMEText
from email.header import Header
from email.utils import COMMASPACE, formatdate

class WarnSender(object):
    def __init__(self, host, port):
        self.smtp = smtplib.SMTP(host, port)
        self.subject = SUBJECT
        self.fromaddr = FROMADDR
        self.toaddrs = EMAIL_ADDRS

    def send_email(self, content):
        msg = MIMEText('<html><head><meta http-equiv="Content-Type" content="text/html; charset=gb2312"/></head><p>%s</p></html>'\
		       % content,'html','gb2312')
        msg['Subject'] = Header(self.subject, 'gb2312')
        msg['From'] = self.fromaddr
        msg['To'] = COMMASPACE.join(self.toaddrs)
	msg['Date'] = formatdate(localtime=True)
        self.smtp.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
	self.smtp.quit()

    def send_sms(self, content):
        server = SMS_SERVER
        phones = PHONES
        for phone in phones:
            subprocess.call("/bin/gsmsend %s %s@%s" % (server, phone, content),
                            shell = True,
                            stdout = open('/dev/null','w'),
                            stderr = subprocess.STDOUT)
