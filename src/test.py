import pyb
import utime
pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
pinC1.low()
utime.sleep(1)
pinC1.high()
