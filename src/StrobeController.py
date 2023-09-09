import machine
import time

MODE_OFF:int = 0
MODE_ON:int = 1
MODE_STATIONARY:int = 2
MODE_NEUTRAL:int = 3 # "neutral", like no signal. Just a bit of pattern.

class StrobeController:

    def __init__(self, gpio:int) -> None:
        self.mode = MODE_OFF
        self.led = machine.Pin(gpio, machine.Pin.OUT)
    
    def start(self) -> None:
        while True:
            time.sleep(0.01)
            if self.mode == MODE_OFF:
                self.led.off()
            elif self.mode == MODE_ON:
                self.led.on()
            elif self.mode == MODE_STATIONARY:

                # turn on
                self.led.on()
                tstart:float = time.time()
                while ((time.time() - tstart) < 1.2):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break

                # turn off
                self.led.off()
                tstart:float = time.time()
                while ((time.time() - tstart) < 2.5):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break
            
            elif self.mode == MODE_NEUTRAL:

                # turn on
                self.led.on()
                tstart:float = time.time()
                while ((time.time() - tstart) < 0.6):
                    time.sleep(0.01)
                    if self.mode != MODE_NEUTRAL:
                        break

                # turn off
                self.led.off()
                tstart:float = time.time()
                while ((time.time() - tstart) < 4.0):
                    time.sleep(0.01)
                    if self.mode != MODE_NEUTRAL:
                        break
            
            else:
                self.led.off()


