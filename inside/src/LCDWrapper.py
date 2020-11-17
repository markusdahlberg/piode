import threading
import time
from RPLCD.gpio import CharLCD
from RPi import GPIO
import piode_send

# Wrapper class for RPI LCD1602 Add-on
class Wrapper:
    lcd = 1
    text = 'Initializing'
    oldtext = text
    shutDownLCD = False

    def __init__(self):
        self.activate()
        workerThread = threading.Thread(target=self.updateScreenWorker, args=(), daemon=True)
        workerThread.start()

    def activate(self):
        # Initialize LCD
        self.lcd = CharLCD(pin_rs=16, pin_e=18, pins_data=[11, 12, 13, 15],
                    numbering_mode=GPIO.BOARD,
                    cols=20, rows=4, dotsize=8,
                    charmap='A02',
                    auto_linebreaks=True,
                    pin_backlight=22)

        self.lcd.clear()
        
        GPIO.output(22, GPIO.HIGH) #turn on LCD backlight

    # Main loop
    def updateScreenWorker(self):
        self.text = "\nReady."
        while not self.shutDownLCD:
            if self.text != self.oldtext:
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write_string(self.text)
                self.oldtext = self.text
            
            time.sleep(1)
            
        self.cleanShutdown()
        

    # If clean shut down is requested, shut down cleanly, and display optional message.
    def cleanShutdown(self, closeMessage=''):
        print('\nshutting down LCD')
        if GPIO.getmode() != None: # If screen can be accessed
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write_string(closeMessage)
            self.lcd.close(clear=False)
        else: # If screen can not be accessed, activate
            self.activate()
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write_string(closeMessage)
            self.lcd.close(clear=False)
        print('complete')
        
