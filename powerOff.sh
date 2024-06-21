
import RPi.GPIO as GPIO
import subprocess
from time import sleep

ledpin = 4
pushpin = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledpin, GPIO.OUT)  # Set LED pin as output (missing in previous code)
GPIO.output(ledpin, GPIO.LOW)  # Turn off LED initially (optional)

def button_press():  # Function name with lowercase first letter
  """
  This function handles the button press event.
  """
  print("Do you want to power off the device? (y/n)")
  choice = input().lower()  # Get user input in lowercase
  if choice == 'y':
    subprocess.call(['sudo', 'poweroff'])
  else:
    print("Power off cancelled.")

try:
  # Main loop
  while True:
    if GPIO.input(pushpin) == GPIO.LOW:  # Button press will cause a LOW signal
      button_press()
    sleep(0.1)  # Add a small delay to avoid excessive button reads

except KeyboardInterrupt:
  GPIO.cleanup()  # Clean up GPIO resources on exit

GPIO.cleanup()  # Clean up GPIO resources before shutting down
