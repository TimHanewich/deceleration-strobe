deceleration_threshold:float = 1.0 # The deceleration, in MPH per second, that you have to be decelerating at for the strobe lights to go into the "decelerating pattern".  Make it positive (i.e. 1.0 is a deceleration of 1.0)
stationary_threshold:float = 10.0 # in MPH. Any speed below this will be considered "stationary" and will play the stationary pattern.

gpio_gps_uart:int = 17 # general purpose pin (GP #, not pin #) that is the receiving data from the NEO-6M GPS module via UART
gpio_led:int = 25 # general purpose pin (GP #, not pin #) that controls the strobe LED (wired to base of transistor)