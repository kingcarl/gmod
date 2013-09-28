from sender import *
import sys, os

def daemonize(func=None, args=(), pidfile=None, startmsg='started with pid %s'):
    sys.stderr.flush()
    sys.stdout.flush()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except IOError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    os.chdir("/")
    os.umask(0)
    os.setsid()
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except IOError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    pid = str(os.getpid())
    sys.stdout.write("\n*%s\n" % startmsg % pid)
    sys.stdout.flush()
    
    #if pidfile:
    #    pf = open(pidfile, 'w+')
    #    pf.write("%s\n" % pid)
    #    pf.close()
    func(args)

def main_loop(args):
    args[0].sr_loop()

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
    	tcpsender = Sender(int(sys.argv[1]))
    	daemonize(func=main_loop, args=(tcpsender,))
    else:
	print "Usage : %s [port]" % sys.argv[0]
	sys.exit(1)
