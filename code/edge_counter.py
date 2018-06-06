#! /usr/bin/python
#-*-coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

in_pin =21
processing_time = 5 # we'll sleep this long to simulate doing other processing
bounce_time_ms =10

rising_edges =0  # define global variables outside of any functions
falling_edges =0

def counter_callback(channel):  # the call back function that runs when an edge is detected
    global rising_edges         # the global tells Python this variable is declared gloablly outside of the function
    global falling_edges
    if GPIO.input (channel) is GPIO.HIGH:
        rising_edges +=1
    else:
        falling_edges +=1
    
"""
to share a global variable between two threads, you need two functions. So instead of a simple script, we define a main
function that runs when the file is opened directly as a main program, not secondarily by sme other program 
"""
def main ():
    GPIO.setwarnings(False)
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(in_pin, GPIO.BOTH, callback = counter_callback ,bouncetime = bounce_time_ms)
    last_rising=0    # keep track of last values, subtract that from total values to get values for this period
    last_falling=0   # has advantage that we write to the global variable from one place, no re-zeroing at top of loop
    while (True):
        try:
            global rising_edges # the global tells Python this variable is declared gloablly outside of the function
            global falling_edges
            sleep (processing_time) # simulates doing other processing
            print ('GPIO pin ' + str (in_pin) + ' went HIGH ' + str (rising_edges- last_rising) + ' times in the last ' + str (processing_time) + ' seconds')
            print ('GPIO pin ' + str (in_pin) + ' went LOW ' + str (falling_edges - last_falling) + ' times in the last ' + str (processing_time) + ' seconds')
            last_rising = rising_edges    # keep track of last values
            last_falling = falling_edges
        except KeyboardInterrupt:
            print ('GPIO pin ' + str (in_pin) + ' went HIGH a total of ' + str (rising_edges) + ' times') # print totals
            print ('GPIO pin ' + str (in_pin) + ' went LOW a total of ' + str (rising_edges) + ' times')
            GPIO.cleanup()
            break

if __name__ == '__main__': # if this is the main file opened, run the main () function
   main()
    
