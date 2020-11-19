from piode_logging import piode_logger
import LCDWrapper
import KeypadHandler
from RPi import GPIO
import time
from datetime import datetime, timedelta
from enum import Enum
import pyudev
import subprocess
import configparser
import os.path

pilog = None

class DiodeStates(Enum):
    IDLE = 1
    EXPORTING = 20
    WAITING = 30


class piode_send:    
    def __init__(self):        
        self.application_active = True #set to false for graceful exit.
        self.LCD = None
        self.Keypad = None
        self.State = DiodeStates.IDLE
        self.trigger_on_filename = None
        self.trigger_on_size = None
        self.trigger_on_any_file = None
        self.trigger_on_button = None
        self.trigger_on_only_button = None
        self.trigger_on_time = None
        self.trigger_on_interval = None
        self.time_of_last_export = time.time()
        self.has_executed_timed_export_today = False
        self.date_last_execution = datetime.today().date() + timedelta(-1)
        self.trigger_on_command_return_zero = None        

        self.check_interval = 2

        self.origin_folder = '/home/pi/data/' # default value for origin folder if path is empty
        self.usb_serial = ''

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)           
        GPIO.setup(37, GPIO.OUT) # Button on Switch Outside

    # Initialize custom logging module
    def init_logging(self):
        global pilog
        pilog = piode_logger(self.LCD)

    # Initialize RPI LCD1602 Add-on
    def init_display(self):        
        self.LCD = LCDWrapper.Wrapper() # Initialize LCD
        self.Keypad = KeypadHandler.Keypad() # Initialize Keypad


    #Check USB memory prescense and identity
    def init_USB(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='block'):            
            if device.get('ID_SERIAL') is not None:
                if device.get('DEVTYPE') == "partition":
                    if self.usb_serial in device.get('ID_SERIAL'): #check that our device has the right serial
                        self.State = DiodeStates.IDLE
                    else:
                        self.State = DiodeStates.WAITING    


    def init(self):
        self.init_display()
        self.init_logging()
        self.init_keypad()
        self.init_USB()  


        #read config file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('/etc/piode/send.conf')

        self.check_interval = int(config['inside']['check_interval'])

        if config['inside']['usb_serial'] != None:
            if config['inside']['usb_serial'] != "":
                self.usb_serial             = config['inside']['usb_serial']

        if config['inside']['origin_folder'] != None:
            if config['inside']['origin_folder'] != "":
                self.origin_folder          = config['inside']['origin_folder']

        self.trigger_on_filename            = self.origin_folder + config['triggers']['exist_filename']

        if config['triggers']['size'] != None:
            if config['triggers']['size'] != "":
                self.trigger_on_size        = int(config['triggers']['size'])

        self.trigger_on_any_file            = config['triggers']['anyfiles']
        self.trigger_on_button              = config['triggers']['physical_button']
        self.trigger_on_only_button         = config['triggers']['only_physical_button']
        self.trigger_on_time                = config['triggers']['time']

        if self.trigger_on_time != None:
            if self.trigger_on_time != "":
                self.trigger_on_time = datetime.strptime(self.trigger_on_time, '%H:%M:%S').time()
            else:
                self.trigger_on_time = None
        
        self.trigger_on_interval    = config['triggers']['interval'] * 60 # multiply value to convert from seconds to minutes.
        
        if self.trigger_on_interval != None:
            if self.trigger_on_interval != "":                
                self.trigger_on_interval    = int(config['triggers']['interval'])
            else:
                self.trigger_on_interval = None
        
        self.trigger_on_command_return_zero = config['triggers']['command_return_0']


    def init_keypad(self):
        self.Keypad = KeypadHandler.Keypad() # Initialize Keypad
        self.Keypad.AddButtonEvent("left", self.button_push)

    def shutdown(self):
        self.LCD.cleanShutdown()

    # Main loop
    def main(self):    
        self.init()
        while self.application_active:
            if self.State == DiodeStates.WAITING:
                pilog.log_info('Waiting')
                self.init_USB()       

            time.sleep(self.check_interval) # Take a break specified amount of seconds

            if self.State == DiodeStates.IDLE:
                pilog.log_info("Ready")
                self.check_triggers() # Check triggers for export

    # Check all export triggers
    def check_triggers(self):

        # Exclusively use trigger button.
        if self.trigger_on_only_button != "True" and self.trigger_on_only_button != "true" and self.trigger_on_only_button != "1":
            if self.trigger_on_filename != None:
                if os.path.isfile(self.trigger_on_filename):
                    pilog.log_debug("Trigger: filename")
                    self.export(0) # commence export.

            # Total size of files in origin folder.
            if self.trigger_on_size != None:            
                if self.folder_size(self.origin_folder) > self.trigger_on_size:
                    pilog.log_debug("Trigger: size")
                    self.export(0) # commence export.

            # Any file present in origin folder.
            if self.trigger_on_any_file != None:
                if self.trigger_on_any_file == "True" or self.trigger_on_any_file == "true" or self.trigger_on_any_file == "1":
                    if sum([len(files) for r, d, files in os.walk(self.origin_folder)]) > 0:
                        pilog.log_debug("Trigger: any files")
                        self.export(0)  # commence export.

            # Every n minutes.
            if self.trigger_on_interval != None:
                if self.trigger_on_interval > 0:
                    if time.time() > self.time_of_last_export + self.trigger_on_interval:
                            pilog.log_debug("Trigger: interval")
                            self.time_of_last_export = time.time()
                            self.export(0) # commence export.
            
            # Every day at specified time.
            if self.trigger_on_time != None:
                if self.date_last_execution < datetime.today().date():
                    if self.trigger_on_time > datetime.now().time():
                        pilog.log_debug("Trigger: time")
                        self.date_last_execution = datetime.today().date()
                        self.export(0) # commence export.

            # If specified process returns 0
            if self.trigger_on_command_return_zero != None:
                if self.trigger_on_command_return_zero != "":                
                    if subprocess.call(self.trigger_on_command_return_zero + "> /dev/null", shell=True) == 0: # if self.trigger_on_command_return_zero comes back with a return code of 0
                        pilog.log_debug("Trigger: external proc.")
                        self.export(0) # commence export.

                

    # Action to run when button is pushed
    def button_push(self, button_id):
        button_name = None
        if button_id == 24:
            button_name = "left"
        if self.trigger_on_button == button_name:
            pilog.log_debug("Trigger: button")
            self.export(0)
        
    # Get folder size
    def folder_size(self, path='.'):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += folder_size(entry.path)
        return total
        

    def export(self, x):
        if self.State != DiodeStates.IDLE:
            pilog.log_debug("System Busy")
        else:
            if sum([len(files) for r, d, files in os.walk(self.origin_folder)]) > 0: #if there are more than 0 files in the origin folder (including subfolders)
                self.State = DiodeStates.EXPORTING # set our state as exporting, which blocks further actions until state is changed to IDLE again
                pilog.log_info("Exporting")

                #Check USB memory prescense and identity
                context = pyudev.Context()
                for device in context.list_devices(subsystem='block'):            
                    if device.get('ID_SERIAL') is not None:
                        if device.get('DEVTYPE') == "partition":
                            if self.usb_serial in device.get('ID_SERIAL'): #check that our device has the right serial
                                subprocess.run('mount '+ device.device_node +' /media/usb -o uid=pi,gid=pi', shell=True) # mount usb device
                    
                                subprocess.run('rm -rf /media/usb/*', shell=True) # remove files from usb device
                                output = subprocess.run('cp -rv ' + self.origin_folder + '* /media/usb/', shell=True, stdout=subprocess.PIPE) # copy files from origin folder to usb device         
                                copied = output.stdout.decode("utf-8") 
                                pilog.log_debug('Files copied')                       
                                pilog.log_debug(copied)
                                                 
                                subprocess.run('cp -rv /var/log/piode-send.log /media/usb/', shell=True) # copy log to usb device
                                
                                #Unmount USB memory
                                subprocess.run('umount -f /media/usb', shell=True) # unmount usb device

                                GPIO.output(37, GPIO.LOW) # "push" USB Switch to other side by simluating
                                time.sleep(1)             # pushing button...
                                GPIO.output(37, GPIO.HIGH) # ...and simulate letting it go
                                time.sleep(3)

                                pilog.log_info("Erasing origin")
                                subprocess.run('rm -rf ' + self.origin_folder + '*', shell=True)  # remove files from origin folder

                                self.State = DiodeStates.WAITING
                                pilog.log_info("Waiting")
                time.sleep(1)
            else:
                pilog.log_info("No files")




if __name__ == "__main__":
    app = piode_send()
    try:
        app.main()
    finally:        
        app.shutdown()