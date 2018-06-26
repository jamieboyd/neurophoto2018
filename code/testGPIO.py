import RPi.GPIO as GPIO
from time import sleep
import Adafruit_MPR121.MPR121 as MPR121

from PTSimpleGPIO import PTSimpleGPIO, Infinite_train
import reaction_time
from RFIDTagReader import RFIDTagReader

"""
beam break test
tag reader
vibration motor with transistor
mpr121 i2c touch breakout and c++ threaded pulses
reacton time
"""
# GPIO pin for beam break
beam_break_pin = 24
# GPIO pin and serial port for tag reader
tag_reader_tir_pin = 23
tag_reader_port = 'serial0'
# global tagreader so we can use it from a callback
tagReader=None
tag =0
# GPIO pin for driving transistor
vibe_motor_pin = 4
# GPIO pins for reaction time task
react_led_pin=13
react_start_pin = 19
react_react_pin = 26
# GPIO Pin for touch sensor IRQ
touch_IRQ_pin = 5 
# Pins for the 4 output tones
tone0_pin = 21
tone1_pin = 20
tone2_pin = 16
tone3_pin = 12
# frequency ratios for a 7th chord are 20:25:30:36
# starting at A 440, or 880, an octave higher:
tone0_freq = 880 
tone1_freq = tone0_freq * (25/20)
tone2_freq = tone0_freq * (30/20)
tone3_freq = tone0_freq * (36/20)
# globals for touch sensor callback
touch_sensor=None
touch_channels =(0,1,2,3)
touch_last_data =0
tones=[]

"""
Threaded call back function on Tag-In-Range pin
Updates tag global variable whenever Tag-In-Range pin toggles
Setting tag to 0 means no tag is presently in range
"""
def tagReaderCallback (channel):
    global tag # the global indicates that it is the same variable declared above and also used by main loop
    global tagReader
    if GPIO.input (channel) == GPIO.HIGH: # mouse just entered
        try:
            tag = tagReader.readTag ()
        except Exception as e:
            print ('Tag Reader error: ', str (e))
            print ('continuing...')
    else:  # mouse just left
        tag = 0


"""
Threaded callback function for touch sensor

"""
def touchSensorCallback (channel):
    global touch_sensor
    global touch_channels
    global touch_last_data
    global tones
    touched = touch_sensor.touched()
    for channel in touch_channels:
        chanBits = 2**channel
        if (touched & chanBits) and not (touch_last_data & chanBits): # new touch
            tones [channel].start_train()
        elif (touch_last_data & chanBits) and not(touched & chanBits): # new un-touch
            tones [channel].stop_train()
            
    touch_last_data = touched
        
"""
Main function loops through a menu presentation, running the function for the selected demo
In most cases, we do the setup for the pins on 
"""
def main():
    # init GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # make sure vibe motor is off
    GPIO.setup (vibe_motor_pin, GPIO.OUT, initial=GPIO.LOW)
    # make a list of inifinite trains to play 4 tones, maybe don't make and destroy threads every time
    global tones
    tones.append (Infinite_train(PTSimpleGPIO.MODE_FREQ, tone0_pin, tone0_freq, 0.5, PTSimpleGPIO.ACC_MODE_SLEEPS_AND_SPINS))
    tones.append (Infinite_train(PTSimpleGPIO.MODE_FREQ, tone1_pin, tone1_freq, 0.5, PTSimpleGPIO.ACC_MODE_SLEEPS_AND_SPINS))
    tones.append (Infinite_train(PTSimpleGPIO.MODE_FREQ, tone2_pin, tone2_freq, 0.5, PTSimpleGPIO.ACC_MODE_SLEEPS_AND_SPINS))
    tones.append (Infinite_train(PTSimpleGPIO.MODE_FREQ, tone3_pin, tone3_freq, 0.5, PTSimpleGPIO.ACC_MODE_SLEEPS_AND_SPINS))
    
    # make a string with the menu used to get user selection
    inputStr = '\n\n----An interactive demo using various hardware with the Raspberry Pi.-----\n'
    inputStr += 'Enter a number from 1 to 5\n'
    inputStr += '1 to demonstrate IR Beam Breaker\n'
    inputStr += '2 to read tags with RFID reader\n'
    inputStr += '3 to turn on/off vibration motor using a transistor\n'
    inputStr += '4 to test your reaction time with buttons and an LED\n'
    inputStr += '5 to use capacitive touch sensor to play tones\n'
    inputStr += ':'
    try:
        while True:
            try:
                event = int (input (inputStr))
            except ValueError:
                print ("That wasn't an integer!")
                continue
            if event == 1:
               beamBreakTest()
            elif event == 2:
                rfidTest()
            elif event == 3:
                vibeMotorTest ()
            elif event == 4:
                reactionTimeTest()
            elif event == 5:
                touchToneTest()
            else:
                print ('That was not an integer from 1 to 5')
                continue
                
    except KeyboardInterrupt:
        print ('Quitting')
    finally:
        GPIO.cleanup()
        

def beamBreakTest():
    print ('The beam breaker uses an infra-red LED/photodiode pair.')
    print ('A comparator across the terminals of the photodiode provides the output.')
    print ('When the photodiode is NOT receiving light from the LED,its output is grounded.')
    print ('When receiving light, the output is disconnected, and can be pulled up to desired output V.')
    GPIO.setup (beam_break_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    print ('Enter ctrl-c to return to main menu')
    if GPIO.input (beam_break_pin) == GPIO.HIGH:
        print ('The beam is NOT blocked')
    else:
        print ('The beam is blocked.')
    try:
        while True:
            if GPIO.input (beam_break_pin) == GPIO.LOW:
                GPIO.wait_for_edge (beam_break_pin, GPIO.RISING, timeout= 100)
                if GPIO.input (beam_break_pin) == GPIO.HIGH:
                    print ('The beam is NOT blocked.')
            else:
                GPIO.wait_for_edge (beam_break_pin, GPIO.FALLING, timeout= 100)
                if GPIO.input (beam_break_pin) == GPIO.LOW:
                    print ('The beam is blocked.')                       
    except KeyboardInterrupt:
        print ('returning to main menu')
    finally:
        GPIO.cleanup(beam_break_pin)


def rfidTest():
    print ('The RFID tag reader from ID-Innovations reads passive 125 kHZ RFID tags.')
    print ('Tags encapsulated in glass can be subcutaneously implanted in mice. Read range is several cm') 
    print ('Tag data is a 12 hexadecimal character id. Communication to host is via serial port')
    print ('Tag-in-range pin is kept high when a tag is in reading range of the reader')
    print ('Enter ctrl-c to return to main menu')
    global tag
    global tagReader
    tagReader = RFIDTagReader('/dev/' + tag_reader_port, doChecksum = False, timeOutSecs = 0.1, kind='ID')
    GPIO.setup (tag_reader_tir_pin, GPIO.IN)
    GPIO.add_event_detect (tag_reader_tir_pin, GPIO.BOTH)
    GPIO.add_event_callback (tag_reader_tir_pin, tagReaderCallback)
    try:
        while True: #Loop with a brief sleep, waiting for a tag to be read
            while tag==0:
                sleep (0.1)
                lastTag = tag
            print ('A tag with ID number ' + str (lastTag) + ' has just entered tag reading range')
            # wait for tag to go away
            while tag != 0:
                sleep (0.1)
            print ('The tag with ID number ' + str (lastTag) + ' has just left tag reading range')
    except KeyboardInterrupt:
        print ('returning to main menu')
        GPIO.remove_event_detect(tag_reader_tir_pin)
        GPIO.cleanup (tag_reader_tir_pin)
        del (tagReader)


   
def vibeMotorTest ():
    print ('For the vibration motor, a weight is mounted on the shaft off-centre, so it shakes when it turns')
    print ('A GPIO pin would not provide enough current to drive this motor directly, so a transistor is used.')
    print ('GPIO output to the transistor base (pin 2) through a 330 ohm resistor gates current from')
    print ('5V source through motor into transistor collector (pin 3), and out of transistor emitter (pin 1) to gnd')
    print ('Enter 1 to turn motor ON, 0 to turn motor OFF, ctrl-c to return to main menu')
    
    try:
        while True:
            event = int (input ())
            if event == 0:
                GPIO.output(vibe_motor_pin, GPIO.LOW)
            elif event == 1:
                GPIO.output(vibe_motor_pin, GPIO.HIGH)
    except KeyboardInterrupt:
        GPIO.output(vibe_motor_pin, GPIO.LOW) # shut off before returning
        print ('returning to main menu')


def reactionTimeTest():
    print ('Using only 2 GPIO inputs and one GPIO output controlled with the RPi.GPIO library,')
    print ('we can control a simple apparatus to measure reaction time.')
    print ('press the button on the left and the LED goes out. When the LED comes on again,')
    print ('try to press the button on the right as fast as possible, using the same finger as before.')
    # all the code is another file, just run its main function with our defined pins
    reaction_time.main(react_led_pin, react_start_pin, react_react_pin)
    print ('returning to main menu')
    

def touchToneTest():
    print ('Adafruit breakout for 10 channel MPR121 capacitive touch sensor with i2c communication and')
    print ('Adafruit code libraries are used to make a 4 key touch sensor. Each key is used to')
    print ('drive a different tone, played from a Python/C module with independent threads for each tone.')
    print ('enter ctrl-c to return to main menu.')
    global touch_sensor
    global tones
    touch_sensor = MPR121.MPR121()
    touch_sensor.begin()
    touch_sensor.set_thresholds (8,4) # as per dirkjan
    # test tones
    for tone in tones:
        tone.start_train()
        sleep (0.2)
    sleep (0.5)
    for tone in tones:
        tone.stop_train()
    # set up input for IRQ interrupt
    GPIO.setup(touch_IRQ_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(touch_IRQ_pin, GPIO.FALLING)
    GPIO.add_event_callback (touch_IRQ_pin, touchSensorCallback)
    try:
        while True:
            sleep (0.1)
    except KeyboardInterrupt:
        print ('returning to main menu')
        # turn off al tones
        for tone in tones:
            tone.stop_train()
        GPIO.remove_event_detect(touch_IRQ_pin)
        GPIO.cleanup (touch_IRQ_pin)
        del touch_sensor
    
    
if __name__ == '__main__':
    main()
