import RPi.GPIO as GPIO
import time

MODE_OFF:int = 0
MODE_ON:int = 1
MODE_STATIONARY:int = 2

class StrobeController:

    def __init__(self, gpio:int) -> None:
        self.mode = MODE_OFF
        self.gpio = gpio
        GPIO.setup(self.gpio, GPIO.OUT)
    
    def start(self) -> None:
        while True:
            time.sleep(0.01)
            if self.mode == MODE_OFF:
                GPIO.output(self.gpio, GPIO.LOW)
            elif self.mode == MODE_ON:
                GPIO.output(self.gpio, GPIO.HIGH)
            elif self.mode == MODE_STATIONARY:

                # turn on
                GPIO.output(self.gpio, GPIO.HIGH)
                tstart:float = time.time()
                while ((time.time() - tstart) < 1.25):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break

                # turn off
                GPIO.output(self.gpio, GPIO.LOW)
                tstart:float = time.time()
                while ((time.time() - tstart) < 2.5):
                    time.sleep(0.01)
                    if self.mode != MODE_STATIONARY:
                        break


