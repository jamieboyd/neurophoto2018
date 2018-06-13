from PTSimpleGPIO import PTSimpleGPIO, Pulse
from RFIDTagReader import RFIDTagReader
from time import sleep


"""
beam break test
tag reader
vibration motor with transistor
mpr121 i2c touch breakout and c++ threaded pulses
reacton time
"""
# for beam break
beam_break_pin = 21
# for tag reader
tag_reader_tir_pin = 25
tag_reader_port = '/dev/serial0'
reader = RFIDTagReader


def main:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    inputStr = '---------------------------------------\n'
    inputStr += 'Enter a number from 1 to 5\n'
    inputStr += '1 to demonstrate IR Beam Breaker\n'
    inputStr += '2 to read tags with RFID reader\n'
    inputStr += '3 to turn on/off vibration motor using a transistor\n'
    inputStr += '4 to test your reaction time'
    inputStr += '5 to use capacitive touch sensor to play tones\n'
    inputStr += ':'
    try:
        while True:
            event = int (input (inputStr))
            if event == 1:
               beamBreakTest()
            elif event == 2:
                rfidTest()
                
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
    print ('checking beam breaker, enter ctrl-c to return to main menu')
    if (GPIO.input (cageSettings.tirPin) == GPIO.HIGH):
        print ('The beam is blocked'.)
    else:
        print ('The beam is NOT blocked'.)
    try:
        while True:
            if (GPIO.input (cageSettings.tirPin) == GPIO.LOW):
                GPIO.wait_for_edge (beam_break_pin, GPIO.RISING timeout= 100)
                if (GPIO.input (cageSettings.tirPin) == GPIO.HIGH):
                    print ('The beam is blocked'.)
            else:
                GPIO.wait_for_edge (beam_break_pin, GPIO.FALLING timeout= 100)
                if (GPIO.input (cageSettings.tirPin) == GPIO.LOW:
                    print ('The beam is NOT blocked'.)                       
    except KeyboardInterrupt:
        print ('returning to main menu')
    finally:
        GPIO.cleanup(beam_break_pin)



def rfidTest():
    print ('The RFID tag reader from ID-Innovations reads passive 125 kHZ RFID tags.')
                    
    
    startTime = time()
    GPIO.wait_for_edge (cageSet.tirPin, GPIO.FALLING, timeout= 10000)
if (time () > startTime + 10.0):
print ('Tag stayed in range for over 10 seconds')
tagError = True


def tFunc (* args):
    print ('test happens')


class Pulse_EF (Pulse):
    
    def endFunc(self, *args):
        print ('test happens', args[0], args[1], args[2])

        
if __name__ == '__main__':

    p1 = Pulse_EF (23, 0, 0.5, 0.5, PTSimpleGPIO.ACC_MODE_SLEEPS_AND_SPINS)
    p1.do_pulse()
    print ('1st pulse started')
    p1.wait_on_busy (2)
    print ('1st pulse done')
    p1.set_endFunc_obj(1, 0, p1)
    ptSimpleGPIO.setEndFuncObj (p1.task_ptr, p1, 1, 0)
    print ('endFunc object set=', p1.has_endFunc())
    p1.endFunc(1,2,3)
    p1.do_pulse()
    print ('2nd pulse started')
    p1.wait_on_busy (2)
    print ('2nd pulse done')
