#! /usr/bin/python
#-*-coding: utf-8 -*-

from time import time, sleep
from datetime import datetime
from random import random
from array import array
import RPi.GPIO as GPIO

# constants
led_pinG =26
start_pinG = 21
react_pinG = 20

bounce_time_ms = 2

max_time = 1000
inter_trial_time = 3 # +/- 1 second for randomization

def flash (led_pin, sleep_time):
    for i in range (0, 10):
        GPIO.output (led_pin, not (GPIO.input (led_pin)))
        sleep (sleep_time)

def main (led_pin, start_pin, react_pin):
    name = input ('Subject Name= ')
    name = name.replace(' ', '_')
    num_trials = int (input ('number of trials='))
    data_array = array('f', [0] * num_trials)

    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup (start_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    GPIO.setup (react_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup (led_pin, GPIO.OUT)

    GPIO.output (led_pin, GPIO.LOW)
    trial = 0
    try:
        for trial in range (0, num_trials):
            # wait for subject to put finger on start button, sending GPIO high
            if GPIO.input (start_pin) is GPIO.LOW:
                print ('Put finger on start button to start a trial')
                while True:
                    result = GPIO.wait_for_edge(start_pin, GPIO.RISING, bouncetime= bounce_time_ms, timeout=100)
                    if result is not None: 
                        break 
            GPIO.output (led_pin, GPIO.HIGH) # turn off LED to signal trial start
            print ('Starting trial # ' + str (trial))
            wait_time = int (1000 * (inter_trial_time + 2 * (0.5 - random())))
            result = GPIO.wait_for_edge(start_pin, GPIO.FALLING, bouncetime= bounce_time_ms, timeout=wait_time)
            if result is not None: # subject lifted finger before LED was lit
                data_array [trial] = -1
                print ('Finger was lifted from start button before LED was lit - trial aborted')
                flash (led_pin, 0.05)
            else: # subject waited with finger on start switch till start time, so turn on LED and start timing
                GPIO.output (led_pin, GPIO.LOW)
                start_time = time()
                result = GPIO.wait_for_edge(react_pin, GPIO.RISING, bouncetime= bounce_time_ms, timeout=max_time)
                end_time= time()
                if result is None:
                    data_array [trial] = -2
                    print ('Reaction button not pressed before time out')
                    flash (led_pin, 0.05)
                else: # subject pressed the react button before time out
                    data_array [trial] = end_time - start_time
                    print ('Measured reaction, time = {:.3f} seconds'.format(data_array [trial]))
                    GPIO.output (led_pin, GPIO.HIGH) # turn off LED to signal good trial
                    sleep (0.5)
                    GPIO.output (led_pin, GPIO.LOW) # turn LED back on again for start of next trial
    except KeyboardInterrupt:
        num_trials = trial
        print ('Remaining trials cancelled after ' + str (num_trials) + ' trials')
    finally:
        flash(led_pin, 0.2)
        GPIO.cleanup()


    dt = datetime.fromtimestamp(time())
    date_str = '{:04}_'.format(dt.year) + '{:02}_'.format (dt.month) + '{:02}'.format (dt.day)
    file_name = '/home/pi/Desktop/' + name + '_' + date_str + ".txt"
    with open (file_name, 'a') as out_file:
        for trial in range (0, num_trials):
            out_file.write ('{:.3f}\n'.format (data_array [trial]))
        out_file.close()
        print ('Finished. Results printed to ' + file_name)


if __name__ == '__main__': # if this is the main file opened, run the main () function
   main(led_pinG, start_pinG, react_pinG)
