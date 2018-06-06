#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Checks repeatedly at 10 Hz to see if GPIO line is low or high
"""
import RPi.GPIO as GPIO # remember to use gksudo for root access
from time import sleep
in_pin = 21
GPIO.setmode(GPIO.BCM)
#GPIO.setup(in_pin,GPIO.IN, pull_up_down = GPIO.PUD_OFF) # no pull-up or pull-down
GPIO.setup(in_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # pull-down resistor
while True:
    try:
        if GPIO.input(in_pin) is GPIO.HIGH:
            print ('GPIO pin ' + str (in_pin) + ' is high')
        else:
           print ('GPIO pin ' + str (in_pin) + ' is low')
        sleep (0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
    

