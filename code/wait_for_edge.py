#! /usr/bin/python
#-*-coding: utf-8 -*-

import RPi.GPIO as GPIO

in_pin =21
bounce_time_ms = 10
time_out_ms = 5000

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup (in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while (True):
    try:
        result = GPIO.wait_for_edge(in_pin, GPIO.BOTH, bouncetime= bounce_time_ms, timeout=time_out_ms)
        if result is None:
            print ('No button press on GPIO pin ' + str (in_pin) + ' for ' + str (time_out_ms/1000) + ' seconds.')
        else:
            if GPIO.input (in_pin) is GPIO.HIGH:
                print ('GPIO pin ' + str (in_pin) + ' went HIGH')
            else:
                 print ('GPIO pin ' + str (in_pin) + ' went LOW')
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
    
            
