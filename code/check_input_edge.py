#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Polls for low-to-high event, then polls for high-to-low event
"""
import RPi.GPIO as GPIO # remember to use gksudo for root access
from time import sleep
in_pin = 21
sleep_time = 0.1 # make shorter for better performance, more CPU usage
GPIO.setmode(GPIO.BCM)
GPIO.setup(in_pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
while True:
    try:
        while GPIO.input(in_pin) is GPIO.LOW:
            pass
            # sleep (sleep_time)
        print ('GPIO pin ' + str (in_pin) + ' went HIGH')
        while GPIO.input(in_pin) is GPIO.HIGH:
            pass
            #sleep (sleep_time)
        print ('GPIO pin ' + str (in_pin) + ' went LOW')
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
