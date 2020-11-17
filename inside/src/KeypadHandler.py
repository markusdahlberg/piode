import threading
import time
from RPi import GPIO

class Keypad:
    active = True

    lastbutton = "None"


    def __init__(self):
        print("Keypad handler init")
        GPIO.setup(24, GPIO.IN)
        GPIO.setup(26, GPIO.IN)
        GPIO.setup(19, GPIO.IN)

        #GPIO.add_event_detect(24, GPIO.FALLING, callback=self.LeftButtonEvent, bouncetime=300)
        #GPIO.add_event_detect(26, GPIO.FALLING, callback=self.UpButtonEvent, bouncetime=300)
        #GPIO.add_event_detect(19, GPIO.FALLING, callback=self.DownButtonEvent, bouncetime=300)

    def AddButtonEvent(self, btn, eventhandler):
        channel = -1
        if btn.lower() == "left" or btn.lower() == "l":
            channel = 24
        elif btn.lower() == "up" or btn.lower() == "u":
            channel = 26
        elif btn.lower() == "down" or btn.lower() == "d":
            channel = 19

        GPIO.add_event_detect(channel, GPIO.FALLING, callback=eventhandler, bouncetime=300)


            