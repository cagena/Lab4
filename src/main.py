import pyb
import utime
import task_share

class Interrupt:
    def __init__(self):

        ## A pin variable to recieve the duty cycles.
        self.pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
        self.pinC0 = pyb.Pin(pyb.Pin.cpu.C0, pyb.Pin.IN)

        self.adc = pyb.ADC(self.pinC0)
        
        # This queue holds unsigned short (16-bit) integers
        self.my_queue = task_share.Queue('H', 1000, name="My Queue")
        
        self.runs = 0
        self.end_flag = 0
        self.time = 0

    def read_adc(self,IRQ_src):
        if self.runs < 500:
            v_out = self.adc.read()
            # Somewhere in one task, put data into the queue
            self.my_queue.put (v_out,in_ISR = True)
            self.runs += 1
        else:
            self.end_flag = 1
            
    def step(self):
        self.pinC1.high()
        while self.my_queue.any():
            utime.sleep_ms(1)
            print('{:},{:}'.format(self.time,self.my_queue.get(in_ISR = True)))
            self.time += 1
            if self.end_flag == 1:
                print('Done')
                self.pinC1.low()

if __name__ == '__main__':
    ## The timer variable for the motor.
    tim = pyb.Timer(1, freq = 1000)
    interrupt = Interrupt()
    tim.callback(interrupt.read_adc)
    utime.sleep_ms(5)
    interrupt.step()
    
