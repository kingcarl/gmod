import logging
import os

class EonsLog:
    def __init__(self, logfile):
        self.logger = logging.getLogger("eons")
        self.logger.setLevel(logging.INFO)
        
        if not os.path.exists(os.getcwd()+'/log/'):
            os.mkdir(os.getcwd()+'/log/')
            
        fh = logging.FileHandler('./log/%s' % logfile)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def DEBUG(self, msg):
        self.logger.debug(msg)
    
    def INFO(self, msg):
        self.logger.info(msg)
        
    def WARN(self, msg):
        self.logger.warn(msg)
        
    def ERROR(self, msg):
        self.logger.error(msg)
        
    def CRITICAL(self, msg):
        self.logger.critical(msg)
        
elogger = EonsLog('eons.log')
    
    
    
