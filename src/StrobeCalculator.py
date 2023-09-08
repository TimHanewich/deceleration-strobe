import StrobeController

class StrobeCalculator:

    def __init__(self) -> None:
        self.mode:int = None
        self._last_speed_mph:float = None
        self._last_ticks_ms:int = None

    def feed(self, speed_mph:float, ticks_ms:int) -> None:

        if self._last_speed_mph != None and self._last_ticks_ms != None:
            acceleration_mph_per_second:float = (speed_mph - self._last_speed_mph) / ((ticks_ms - self._last_ticks_ms)/1000)
            if speed_mph < 10.0: # we are stationary, or below 10 MPH, so put on the stationary mode.
                self.mode = StrobeController.MODE_STATIONARY
            elif acceleration_mph_per_second < 1.0: # shaving off 1 MPH per second
                self.mode = StrobeController.MODE_ON
            else: # not decelerating hard enough. So turn off!
                self.mode = StrobeController.MODE_OFF
        else: # no good data.
            self.mode = StrobeController.MODE_NEUTRAL # so just go neutral.

        # Set last
        self._last_speed_mph = speed_mph
        self._last_ticks_ms = ticks_ms