import logging
from datetime import datetime

# Custom logging class that wraps conventional logging and adds output to LCD.
class piode_logger:
    def __init__(self, lcd):
        # Initialize logger.
        self.logger = logging.getLogger('piode-send')
        self.logger.setLevel(logging.DEBUG)
        self.fileHandler = logging.FileHandler('/var/log/piode-send.log')
        self.fileHandler.setLevel(logging.DEBUG)
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(logging.DEBUG)
        
        # Add handlers for logfile and console output.
        self.logger.addHandler(self.fileHandler) 
        self.logger.addHandler(self.consoleHandler)

        # Format output to file and console in standard way
        self.formatter = logging.Formatter('%(asctime)s  piode-send  %(levelname)s: %(message)s')
        self.fileHandler.setFormatter(self.formatter)
        self.consoleHandler.setFormatter(self.formatter)

        self.display = lcd

    # Display log message on LCD
    def log_to_display(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")        
        if len(message) > 16:
            message = message[:14] + '..'
        self.display.text = current_time + '\r\n' + message

    # Wrappers for log functions
    def log_info(self, message):
        self.log_to_display(message) # Display message on LCD.
        self.logger.info(message)    # Write message to regular log outputs.

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
