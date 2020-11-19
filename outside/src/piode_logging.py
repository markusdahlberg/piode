import logging
from datetime import datetime

class piode_logger:
    def __init__(self, lcd):
        self.logger = logging.getLogger('piode-receive')
        self.logger.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler('/var/log/piode-receive.log')
        self.fileHandler.setLevel(logging.DEBUG)
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(logging.DEBUG)
        
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.consoleHandler)

        self.formatter = logging.Formatter('%(asctime)s  piode-receive  %(levelname)s: %(message)s')
        self.fileHandler.setFormatter(self.formatter)
        self.consoleHandler.setFormatter(self.formatter)

        self.display = lcd

    def log_to_display(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")        
        if len(message) > 16:
            message = message[:14] + '..'
        self.display.text = current_time + '\r\n' + message

    def log_info(self, message):
        self.log_to_display(message)
        self.logger.info(message)

    def log_debug(self, message):
        self.log_to_display(message)
        self.logger.debug(message)
    
    def log_warning(self, message):
        self.log_to_display(message)
        self.logger.warning(message)
    
    def log_error(self, message):
        self.log_to_display(message)
        self.logger.error(message)
    
    def log_critical(self, message):
        self.log_to_display(message)
        self.logger.critical(message)
