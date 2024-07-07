import pigpio
import time

RX_pin = 27
TX_pin =28
baudrate = 9600 # GPS module baudrate is 9600

pi = pigpio.pi() # Connect to the local Pi's GPIO

if not pi.connected:
    exit() # Exit if the connection failed

pi.bb_serial_read_open(RX_pin, baudrate)

try:
    while True:
        (count, data) = pi.bb_serial_read(RX_pin) # Read the data from the RX pin
        if count > 0: # If there is data available
            try:
                print(data.decode('utf-8')) # Decode the data from bytes to string
            except UnicodeDecodeError:
                print(data)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

pi.bb_serial_read_close(RX_pin)
pi.stop()