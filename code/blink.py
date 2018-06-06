#! /usr/bin/python
#-*-coding: utf-8 -*-

"""
Blinks an LED
"""
import RPi.GPIO as GPIO # remember to use gksudo for root access
from time import sleep # used for timing LED on and off periods

out_pin = 26
on_time = 0.5
off_time= 0.5
blinks = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(out_pin,GPIO.OUT)
for blink in range (0, blinks):
    GPIO.output(out_pin,GPIO.HIGH)
    sleep (on_time)
    GPIO.output(out_pin,GPIO.LOW)
    sleep (off_time)

GPIO.cleanup ()
