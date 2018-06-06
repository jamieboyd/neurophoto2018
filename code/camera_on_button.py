#! /usr/bin/python
#-*-coding: utf-8 -*-

import RPi.GPIO as GPIO
import picamera
from time import time, sleep
from datetime import datetime


in_pin =21
bounce_time_ms = 10
max_movie_time = 10000

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup (in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.preview_fullscreen = False
camera.preview_window = (20, 40, 680, 500) # left, top, right, bottom

base_name = 'trial_'
trial_num = 0
isRecording = False
try:
    while True:
        result = GPIO.wait_for_edge(in_pin, GPIO.FALLING, bouncetime= bounce_time_ms, timeout = 1000)
        if result is None:
            continue
        camera.start_recording(base_name + str(trial_num) + '.h264')
        startSecs= time() # time() returns seconds since 1970/01/01
        camera.start_preview()
        isRecording = True
        print ('Started recording ' + base_name + str(trial_num) + '.h264 at ' + datetime.fromtimestamp (int(startSecs)).isoformat (' '))
        timed_out = not GPIO.wait_for_edge(in_pin, GPIO.FALLING, bouncetime= bounce_time_ms, timeout=max_movie_time)
        camera.stop_recording()
        endSecs = time()
        camera.stop_preview()
        isRecording = False
        if timed_out:
            print ('movie ' + base_name + str(trial_num) + '.h264 stopped because of time out after ' + str( endSecs -startSecs) + ' seconds')
        else:
            print ('movie ' + base_name + str(trial_num) + '.h264 stopped because of button up after ' + str( endSecs -startSecs) + ' seconds')
        trial_num +=1
except KeyboardInterrupt:
    if isRecording:
        camera.stop_recording()
        camera.stop_preview()
    camera.close()
    GPIO.cleanup()

