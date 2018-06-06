from PTSimpleGPIO import PTSimpleGPIO, Pulse
import ptSimpleGPIO
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
