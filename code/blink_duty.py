
"""
Blinks an LED with an increasing duty cycle
"""
import RPi.GPIO as GPIO # remember to use gksudo for root access
from time import sleep # used for timing LED on and off periods

the_pin = 21
pulse_time = 0.2
blinks = 100
pulse_incr = pulse_time/blinks
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(the_pin,GPIO.OUT)
for blink in range (0, blinks):
    on_time = blink * pulse_incr
    off_time = pulse_time  - on_time
    GPIO.output(21,GPIO.HIGH)
    sleep (on_time)
    GPIO.output(21,GPIO.LOW)
    sleep (off_time)

GPIO.cleanup ()
