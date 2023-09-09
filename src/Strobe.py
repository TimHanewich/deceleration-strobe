import StrobeController
import settings
import machine
import time

MODE_OFF:int = 0
MODE_ON:int = 1
MODE_STATIONARY:int = 2
MODE_NEUTRAL:int = 3 # "neutral", like no signal. Just a bit of pattern.

class StrobeCalculator:

    def __init__(self) -> None:
        self.mode:int = None
        self._last_speed_mph:float = None
        self._last_ticks_ms:int = None

    def feed(self, speed_mph:float, ticks_ms:int) -> None:
        if self._last_speed_mph != None and self._last_ticks_ms != None and ticks_ms > self._last_ticks_ms:
            acceleration_mph_per_second:float = (speed_mph - self._last_speed_mph) / ((ticks_ms - self._last_ticks_ms)/1000)
            if acceleration_mph_per_second < (settings.deceleration_threshold * -1): # shaving off X MPH per second
                self.mode = StrobeController.MODE_ON
            elif speed_mph < settings.stationary_threshold: # we are stationary, or below 10 MPH, so put on the stationary mode.
                self.mode = StrobeController.MODE_STATIONARY
            else: # not decelerating hard enough. So turn off!
                self.mode = StrobeController.MODE_OFF
        else: # no good data.
            self.mode = StrobeController.MODE_NEUTRAL # so just go neutral.

        # Set last
        self._last_speed_mph = speed_mph
        self._last_ticks_ms = ticks_ms

class StrobeController:

    def __init__(self, gpio:int) -> None:
        self.mode = MODE_OFF
        self.led = machine.Pin(gpio, machine.Pin.OUT)
    
    def start(self) -> None:
        while True:
            time.sleep(0.001)
            if self.mode == MODE_OFF:
                self.led.off()
            elif self.mode == MODE_ON:
                self.led.on()
            elif self.mode == MODE_STATIONARY:

                # turn on
                self.led.on()
                tstart:int = time.ticks_ms()
                while ((time.ticks_ms() - tstart) < 1200):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break

                # turn off
                self.led.off()
                tstart:int = time.ticks_ms()
                while ((time.ticks_ms() - tstart) < 2500):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break
            
            elif self.mode == MODE_NEUTRAL:

                # turn on
                self.led.on()
                tstart:int = time.ticks_ms()
                while ((time.ticks_ms() - tstart) < 500):
                    time.sleep(0.01)
                    if self.mode != MODE_NEUTRAL:
                        break

                # turn off
                self.led.off()
                tstart:int = time.ticks_ms()
                while ((time.ticks_ms() - tstart) < 2000):
                    time.sleep(0.01)
                    if self.mode != MODE_NEUTRAL:
                        break
            
            else:
                self.led.off()


