import time
import serial

# Configure connection. Replace 'COM3' with your actual Arduino port.
# Keep timeout=1 so the code doesn't hang indefinitely.
arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)

# CRITICAL: Wait 2 seconds for the Arduino to finish resetting.
# If you don't wait, pattern_1() will interrupt your command!
time.sleep(2)

print("Sending 'R' command to blink LED on pin 2...")
# Send the string 'R' followed by the newline character your Arduino expects
arduino.write("R'\n".encode("utf-8"))

# Cleanly close the serial port connection
arduino.close()
print("Connection closed.")