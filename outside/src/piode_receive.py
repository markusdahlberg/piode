from piode_logging import piode_logger
import pyudev
import subprocess
import os
import time
from RPi import GPIO
import LCDWrapper
import configparser


pilog = None

class piode_receive:    
    def __init__(self):      
        self.LCD = None
        GPIO.setmode(GPIO.BOARD)   
        GPIO.setup(37, GPIO.OUT) # Button on Switch inside
        GPIO.output(37, GPIO.HIGH)

        self.run_after_receiving = None
        self.erase_after_receiving = None

    def init(self):
        self.init_display()
        self.init_logging()

        #read config file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('/etc/piode/receive.conf')

        self.run_after_receiving = config['receive']['action_after_receive']
        self.erase_after_receiving = config['receive']['erase_after_receive']
        time.sleep(1)

    def init_logging(self):
        global pilog
        pilog = piode_logger(self.LCD)

    def init_display(self):        
        self.LCD = LCDWrapper.Wrapper() # Initialize LCD

    def shutdown(self):
        self.LCD.cleanShutdown()
    
    def USBAdded(self, device):
        # Mount usb drive
        pilog.log_debug('Mounting device')
        subprocess.run('mount '+ device.device_node +' /media/usb -o uid=pi,gid=pi', shell=True)
        time.sleep(2)

        # Copy log file to usb device

        # Package files
        pilog.log_info('Archiving files')
        subprocess.run('tar -zcvf /home/pi/export/export.tar.gz -C /media/usb/ .', shell=True)
        time.sleep(2)
        
        # Delete files from USB
        pilog.log_debug('Erasing storage')
        subprocess.run('rm -rf /media/usb/*', shell=True)
        time.sleep(2)

        # Unmount USB
        pilog.log_debug('Unmounting device')
        subprocess.run('umount -f /media/usb', shell=True)

        # Perform action
        if self.run_after_receiving != "":
            pilog.log_info("Custom action")
            subprocess.run(self.run_after_receiving, shell=True)

        # Erase
        if self.erase_after_receiving == "True" or self.erase_after_receiving == "true" or self.erase_after_receiving == "1":
            pilog.log_info("Erasing files")
            erase_result = subprocess.run('rm -rf /home/pi/export/*', shell=True)
            pilog.log_debug("erase response: " + str(erase_result))

        GPIO.output(37, GPIO.LOW)
        time.sleep(1)
        GPIO.output(37, GPIO.HIGH)
        pilog.log_debug('Ready')


    def main(self):
        self.init()
        pilog.log_info('Ready')
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')

        time.sleep(1)
        pilog.log_info('Monitoring USB')
        for device in iter(monitor.poll, None):
            if device.get('ID_SERIAL') is not None:
                if device.get('DEVTYPE') == "partition":
                    if device.action == "add":
                        pilog.log_debug('Device added')
                        self.USBAdded(device)


if __name__ == "__main__":
    app = piode_receive()
    try:
        app.main()
    finally:        
        app.shutdown()