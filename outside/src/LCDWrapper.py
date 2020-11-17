import threading
import time
from RPLCD.gpio import CharLCD
from RPi import GPIO


class Wrapper:
    i = 0
    lcd = 1
    text = 'Initializing'
    oldtext = text
    shutDownLCD = False

    def __init__(self):
        self.activate()
        workerThread = threading.Thread(target=self.updateScreenWorker, args=(), daemon=True)
        workerThread.start()

    def activate(self):
        self.lcd = CharLCD(pin_rs=16, pin_e=18, pins_data=[11, 12, 13, 15],
                    numbering_mode=GPIO.BOARD,
                    cols=20, rows=4, dotsize=8,
                    charmap='A02',
                    auto_linebreaks=True,
                    pin_backlight=22)
        self.lcd.clear()
        GPIO.output(22, GPIO.HIGH) #turns on backlight

    def updateScreenWorker(self):
        self.text = "Ready."
        while not self.shutDownLCD:
            #print("Text = " + self.text + "    Oldtext = " + self.oldtext)
            if self.text != self.oldtext:
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write_string(self.text)
                self.i=self.i+1
                self.oldtext = self.text
            
            time.sleep(1)
            
        self.cleanShutdown()
        

    def cleanShutdown(self, closeMessage=''):
        print('\nshutting down LCD')
        if GPIO.getmode() != None:
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write_string(closeMessage)
            self.lcd.close(clear=False)
        else:
            self.activate()
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write_string(closeMessage)
            self.lcd.close(clear=False)
        print('complete')
        
