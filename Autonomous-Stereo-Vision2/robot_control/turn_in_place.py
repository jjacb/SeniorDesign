import serial
import time

# Open a serial connection to Roomba
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200)

# Assuming the robot is awake, start safe mode so we can hack.
ser.write('\x83')
time.sleep(.1)

#Have the robot turn in place for 1 second
values = bytearray([137, 255, 56, 1, 244])
ser.write(values)

time.sleep(5)


# Close the serial port; we're done for now.
ser.close()

