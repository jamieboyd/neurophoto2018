#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Checks repeatedly at 10 Hz to see if GPIO line is low or high
"""
import RPi.GPIO as GPIO # remember to use gksudo for root access
from time import sleep
in_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(in_pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
last_level = GPIO.input (in_pin)
while (True):
    try:
        if GPIO.input(in_pin) is GPIO.HIGH and last_level is GPIO.LOW:
            print ('GPIO pin ' + str (in_pin) + ' went HIGH')
            last_level = GPIO.HIGH 
        elif GPIO.input(in_pin) is GPIO.LOW and last_level is GPIO.HIGH:
           print ('GPIO pin ' + str (in_pin) + ' went LOW')
           last_level = GPIO.LOW 
        sleep (0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
