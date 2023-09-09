import NMEA
import machine
import time
import _thread
import settings
import strobe

print("Deceleration Strobe - Copyright Tim Hanewich 2023")

# set up strobe controller
sc = strobe.StrobeController(settings.gpio_led) # pin number of the LED wire
sc.mode = strobe.MODE_NEUTRAL
_thread.start_new_thread(sc.start, ())
print("Strobe controller set up and running! Beginning with neutral pattern.")

# set up class to read NMEA data
n = NMEA.NMEAParser()
print("NMEA parser set up!")

# set up the strobe calculator
calculator:strobe.StrobeCalculator = strobe.StrobeCalculator()
print("Strobe Calculator set up!")

# set up to receive NMEA data from NEO-6M
gps = machine.UART(0, rx=machine.Pin(settings.gpio_gps_uart), baudrate=9600) # pin number of the UART pin to receive data from NEO-6M GPS module
print("UART bus set up!")
print("Entering infinite loop...")
while True:
    print(str(time.ticks_ms()) + ": Reading from GPS...")
    data = gps.read()
    if data != None:
        print(str(len(data)) + " bytes read!")
        try:
            data2:str = data.decode()
            print("Data received: " + data2)

            print("Feeding data to parser...")
            n.feed(data2)

            # if we have data
            if (time.ticks_ms() - n.speed_last_updated_ticks_ms) < 5000: # if we have data that is newer than 5 seconds old.
                print("Data is new! Current speed: " + str(n.speed_mph) + " MPH. Feeding to strobe calculator...")
                calculator.feed(n.speed_mph, n.speed_last_updated_ticks_ms)
                sc.mode = calculator.mode
                print("StrobeController set to mode '" + str(calculator.mode) + "'")
            else: # if we do not have any data...
                print("Data is nonexistent or old! Going to neutral pattern...")
                sc.mode = strobe.MODE_NEUTRAL # neutral mode (pulse every few seconds briefly)

        except Exception as e:
            print("FAILURE!!! " + str(e))
    else:
        print("Null received from UART pin. Is the NEO-6M connected properly?")
    
    time.sleep(1.0)

