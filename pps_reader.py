import pigpio
import time

pps_pin = 25

# Callback function to be called when a PPS signal is detected
def callback(gpio, level, tick):
    print(f"PPS Detected at {time.time()}")

pi = pigpio.pi()

if not pi.connected:
    exit()

# Set the PPS pin as input with the pull-down resistor enabled
pi.set_mode(pps_pin, pigpio.INPUT) 
pi.set_pull_up_down(pps_pin, pigpio.PUD_DOWN)

pi.callback(pps_pin, pigpio.EITHER_EDGE, callback)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass

pi.stop()