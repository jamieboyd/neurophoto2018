#! /usr/bin/python
#-*-coding: utf-8 -*-

from time import time, sleep
from datetime import datetime
from random import random
from array import array
import RPi.GPIO as GPIO

# constants
start_pin = 21
react_pin = 23
led_pin =26

bounce_time_ms = 10
max_time = 1000
inter_trial_time = 3 # +/- 1 second for randomization

name = input ('Subject Name= ')
name = name.replace(' ', '_')
num_trials = int (input ('number of trials='))
data_array = array('f', [0] * num_trials)

GPIO.setmode (GPIO.BCM)
GPIO.setup (start_pin, GPIO.IN, pud_up_down = GPIO.PUD_DOWN)

GPIO.setup (react_pin, GPIO.IN, pud_up_down = GPIO.PUD_DOWN)
GPIO.setup

GPIO.output (led_pin, GPIO.HIGH)
for trial in range (0, num_trials):
    while True:
        result = GPIO.wait_for_edge(start_pin, GPIO.RISING, bouncetime= bounce_time_ms, timeout=0.1)
        if result is not None:
            break
    GPIO.output (led_pin, GPIO.LOW)
    print ('Starting trial # ' + str (trial))
    wait_time = int (1000 * (inter_trial_time + 2 * (0.5 - random())))
    result = GPIO.wait_for_edge(start_pin, GPIO.FALLING, bouncetime= bounce_time_ms, timeout=wait_time)
    if result is not None: # subject lifted finger before LED
        data_array [trial] = -1
        print ('start position was lifted before LED was lit - trial aborted')
    else: # subject waited with finger on start switch till start time
        GPIO.output (led_pin, GPIO.HIGH)
        start_time = time()
        result = GPIO.wait_for_edge(react_pin, GPIO.RISING, bouncetime= bounce_time_ms, timeout=max_time)
        end_time= time()
        if result is None:
            data_array [trial] = -2
            print ('button not pressed before time out')
        else: # subject pressed the react button before time out
            data_array [trial] = end_time - start_time
            print ('Good reaction, time = {:.3f} seconds'.format(data_array [trial]))
 

dt = datetime.fromtimestamp(time())
date_str = '{:04}_'.format(dt.year) + '{:02}_'.format (dt.month) + '{:02}'.format (dt.day)
filename = '/home/pi/Documents/' + name + '_' + date_str
with open (file_name, 'a') as out_file:
    
    
