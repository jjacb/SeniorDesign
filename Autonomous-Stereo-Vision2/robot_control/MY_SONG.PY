import serial
import time

# Open a serial connection to Roomba
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200)

# Assuming the robot is awake, start safe mode so we can hack.
ser.write('\x83')
time.sleep(.1)

# Program a five-note start song into Roomba.
#ser.write('\x8c\x00\x05C\x10H\x18J\x08L\x10O\x20')
#	            8c  00 05 C  10 H  18 J  8 L  10 O  20
values = bytearray([140,0, 5, 67,16,72,24,74,8,76,16,79,32])
ser.write(values);

# Play the song we just programmed.
ser.write('\x8d\x00')
time.sleep(1.6) # wait for the song to complete

# Leave the Roomba in passive mode; this allows it to keep
#  running Roomba behaviors while we wait for more commands.
ser.write('\x80')

# Close the serial port; we're done for now.
ser.close()
