import serial
import time
import math
import struct
#Given a velocity and  angular velocity in m/s, and serial connection -controls the robot
def drive(vel, ang_vel,ser):
	wheel_radius = .036	#Wheel radius in meters
	wheel_dist = .235	#Distance between wheels
	
	#Constants for tuning how the robot controls
	ang_vel = float(ang_vel*.73) #its over turning
	vel = float(vel*1)
	
	#Calculate the wheel velocity for each wheel
	vel_right = vel - (ang_vel*wheel_dist/2)
	vel_left = vel + (ang_vel*wheel_dist/2)
	
	#Constants to correct for drift
	vel_left = vel_left	
		
	print "Vel left:" + str(vel_left)
	print "Vel right:" + str(vel_right)
	
	#Check to make sure that the velocities are within safe values
	if vel_right > .5:
		print('WARNING - Speed set too high! Lowering speed...')	
		vel_right = .5
	elif vel_right < -.5:
		print('WARNING - Speed set too high! Lowering speed...')	
		vel_right = -.5
		
	if vel_left > .5:
		print('WARNING - Speed set too high! Lowering speed...')	
		vel_left = .5
	elif vel_left < -.5:
		print('WARNING - Speed set too high! Lowering speed...')	
		vel_left = -.5
	
	#Multiply each velocity by 1000 to get them in mm/s and round down to the nearest int
	vel_right = math.floor(1000*vel_right)
	vel_left = math.floor(1000*vel_left)
	
	#Parse out the bytes
	rhigh_byte,rlow_byte = get_bytes(vel_right)
	lhigh_byte,llow_byte = get_bytes(vel_left)
	values = bytearray([145,int(rhigh_byte,2), int(rlow_byte,2), int(lhigh_byte,2),int(llow_byte,2)])
	ser.write(values)
	return values

	
def get_bytes(n):
	#Convert to 16-bit signed 2byte number
	s16 = (int(abs(n)) +2**15) % 2**16 -2**15
	is_neg = 0
	if n < 0:
		is_neg=1
	
	#Conert the number into a binary string
	bin_str = bin(s16)
	#If the string is less than 16+2 chars we need to pad it with 0's (the 2 is for the 0b at the front)
	if len(bin_str) < 18:
		added_zeros = 18 - len(bin_str)
		zero_string = ""
		for i in range(0,added_zeros):
			zero_string = zero_string + "0"
		bin_str = '0b' + zero_string + bin_str[2:]
	#print("Binary string")
	#print(bin_str)	

	#If the number is negative we need to flip the bits and add 1
	if is_neg == 1:
		flipped_bin_string = "0b"
		#Flip all the bits
		for i in range(2,18):
			if bin_str[i] == '0':
				flipped_bin_string = flipped_bin_string + "1"
			else:
				flipped_bin_string = flipped_bin_string + "0"
		bin_str = flipped_bin_string
		#print("Flipped String")
		#print(bin_str)
		
		#Now add 1
		reverse_str = ""
		done = 0
		for i in range(17,1,-1):
			if(done == 0):
				if(bin_str[i] == '0'):
					reverse_str = reverse_str + "1"
					done = 1		
				else:
					reverse_str = reverse_str + "0"
			else:
				reverse_str = reverse_str + bin_str[i]
		reverse_str = reverse_str + "b0"
		#Ok now reverse the string to get the correct 16bit string
		bin_str = reverse_str[::-1]
		#print("Final binary string")
		#print (bin_str)
	
	#Split the 16bit number into two one byte binary strings
	high_byte =  bin_str[:10]
	low_byte = "0b" +  bin_str[10:]
	print(high_byte)
	print(low_byte)	
	
	return high_byte,low_byte
# Open a serial connection to Roomba
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200)
#Start safe mode so we can control
ser.write('\x83')
time.sleep(.1)
#Tell it to drive
drive(.25,0,ser)
time.sleep(4)
# Leave the Roomba in passive mode; this allows it to keep
#  running Roomba behaviors while we wait for more commands.
ser.write('\x80')

# Close the serial port; we're done for now.
ser.close()

