#! /usr/bin/python
#-*-coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

in_pin =21
processing_time =1
bounce_time_ms =10
time_out_ms = 5000

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup (in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(in_pin, GPIO.BOTH, bouncetime = bounce_time_ms)
while (True):
    try:
        sleep (processing_time) # simulates doing other processing
        result = GPIO.event_detected(in_pin)
        if result is True:
            if GPIO.input (in_pin) is GPIO.HIGH:
                print ('GPIO pin ' + str (in_pin) + ' went HIGH at some point in last ' + str (processing_time) + ' seconds')
            else:
                 print ('GPIO pin ' + str (in_pin) + ' went LOW at some point in last ' + str (processing_time) + ' seconds')
        else:
            print ('No activity on GPIO pin ' + str (in_pin) + ' in last ' + str (processing_time) + ' seconds')
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
    
