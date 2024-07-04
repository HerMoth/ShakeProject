import pigpio

RX_pin = 36
TX_pin =38
baudrate = 9600 # GPS module baudrate is 9600

pi = pigpio.pi() # Connect to the local Pi's GPIO

if not pi.connected:
    exit() # Exit if the connection failed

pi.bb_serial_read_open(RX_pin, baudrate)

try:
    while True:
        (count, data) = pi.bb_serial_read(RX_pin) # Read the data from the RX pin
        if count > 0: # If there is data available
            print(data.decode('utf-8')) # Decode the data from bytes to string
except KeyboardInterrupt:
    pass

pi.bb_serial_read_close(RX_pin)
pi.stop()