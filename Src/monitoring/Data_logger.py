import serial
import time
import RPi.GPIO as gpio
import os
import pigpio
"""
Error LED table
2 flash - waiting for GPS
3 flash - warm up for air quality
on then off - Logging (everything okay)

LED out is used to know which state the hardware is currently in
"""
def led_out(flashes):
	for i in range(0,flashes):
		gpio.output(24,1)
		time.sleep(0.25)
		gpio.output(24,0)
		#If the LED is just going on once, no need to wait
		if flashes is not 0:
			time.sleep(0.25)
#______________________________________SERIAL________________________________________________#
#format of gps message is (DDMM.MMMM) needs to be DD + MM.MMMM/60
def change_format_of_GPS(GPS_measurement):
	degree = int(GPS_measurement/100)
	minutes = GPS_measurement % 100
	#limit to 5 dp
	return format(degree + (minutes/60),'.5f')

#requests message from serial and puts it in a dictionary, only returns once a position is fixed

def get_and_translate_gpgga(serial):
	message = ''
	while True:
		while "GPGGA" not in message:
			#request message and decode + remove endline
			message = serial.readline().decode('utf-8').replace('\r\n','')

		#zip message into dictionary
		gpgga_message = dict(zip(["message_ID",
							"timestamp",
							"latitude",
							"ns_indicator",
							"longitude",
							"ew_indicator",
							"position_fix_indicator",
							"satellites_used",
							"HDOP",
							"msl_altitude",
							"units",
							"geoal_seperation",
							"units",
							"age_of_diff_corr",
							"checksum"],message.split(",")))
		#only break when a fix is found
		if gpgga_message.get("position_fix_indicator") is '1':
			break
		else:
			led_out(2)
			

	return gpgga_message

#set up serial with GPIO config settings
def set_up_serial():
	
	gpio.setup(12,gpio.OUT)
	serial_complete = serial.Serial(
			   port='/dev/ttyS0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
	)
	#get gpgga message once to ensure there is a gps fix
	print("waiting for GPS fix")
	get_and_translate_gpgga(serial_complete)
	return serial_complete

#______________________________________AIR QUALITY________________________________________________#
#get data from air qualty sensor 
def get_air_quality_data(pi,handle):
	i2c_read_bytes = 9
	byte_when_ready = 0x00
	warm_up = True
	
	while warm_up:
		count, data = pi.i2c_read_device(handle, i2c_read_bytes)
		while count < i2c_read_bytes:
			time.sleep(10)
		try:
			#air quality message [2] is 0 when ready 
			if data[2] is byte_when_ready:
				warm_up = False
			else:
				print("Air Quality Sensor in warm up state")
				led_out(3)
				time.sleep(20)
		except Exception as e:
			raise e
		
	return data
#standard 2 byte to variable conversion
def translate_air_data(data):
	co2 = (data[0]*256)+data[1]
	toc = (data[7]*256)+data[8]
	return co2, toc
#open the communication with the i2c bus using pigpio
def set_up_i2c():
	i2c_bus = 1
	i2c_address = 0x5a

	pi = pigpio.pi()
	if not pi.connected:
		pi.close()
		exit()
	handle = pi.i2c_open(i2c_bus, i2c_address)
	get_air_quality_data(pi,handle)
	return pi, handle


#______________________________________Directory Functions________________________________________________#

#needs to check for files that were open when RPi shuts down. Removes '~' from start of the file names
def check_previous_files():
	#get all files and folders in /logs folder
	for root, dirs,files in os.walk(os.getcwd() + '/logs'):
		#loop through all files
		for filename in files:
			#removes ~ from file names
			if filename.startswith('~'):
				filenamelogs = os.getcwd() + '/logs/' + filename
				os.rename(filenamelogs,filenamelogs.replace('~',''))
#set up log file
def set_up_dir():
	logs_dir = os.getcwd() + '/logs'
	#make folder if its not there
	if not os.path.exists(logs_dir):
		os.makedirs(logs_dir)
	#use date and time to create a log file
	file_path = logs_dir + '/~log ' + str(time.strftime("%c")) + '.txt'
	#remove invalid symbols for directories
	file_path = file_path.replace(':','')
	#open file
	file = open(file_path,'a')
	file.write('timestamp,lat,long,pos_fix,CO2,TOC\r\n')
	file.close()
	return file_path
	
#______________________________________Logging________________________________________________#
#gets messages and logs them in a file
def start_logging(file, serial,pi,handle):
	#get gps and air quality message
	gpgga_message = get_and_translate_gpgga(serial)
	air_quality_message = get_air_quality_data(pi,handle)
	#get co2 and toc values from bytes
	co2 , toc = translate_air_data(air_quality_message)

	#reformat data 
	gpgga_message['latitude'] = change_format_of_GPS(float(gpgga_message.get('latitude')))
	gpgga_message['longitude'] = change_format_of_GPS(float(gpgga_message.get('longitude')))
	#use indicators to change south and west values to negative
	if gpgga_message.get('ns_indicator') is 'S':
		gpgga_message['latitude'] = str(float(gpgga_message.get("latitude"))*-1)
	if gpgga_message.get('ew_indicator') is 'W':
		gpgga_message['longitude'] = str(float(gpgga_message.get("longitude"))*-1)

	
	#write to file
	file.write(gpgga_message.get("timestamp") + ','
				+ str(float(gpgga_message.get("latitude"))) + ','
				+ gpgga_message.get("longitude") + ','
				+ gpgga_message.get("position_fix_indicator") + ','
				+ str(co2) + ','
				+ str(toc) + '\r\n')
	led_out(1)


#______________________________________Main________________________________________________#
		
def main():
	#set gpio settings
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	gpio.setwarnings(False)
	
	print("Checking previous files")
	check_previous_files()
	print("setting variables...")
	#variables for i2c
	
	#largest kb file size
	largest_file_size_kb = 25
	
	print("setting i2c interface...")
	pi, handle = set_up_i2c()
	print("setting serial interface...")
	serial = set_up_serial()
	logging = True
	while logging:
		print("creating file...")
		file_path = set_up_dir()
		print("Logging starting...")
		#while file size is less than largest file size - log
		while os.path.getsize(file_path)/1024 < largest_file_size_kb:
			#open the file to append 'a'
			file = open(file_path,'a')
			#for presenting
			print("filesize: " + str(os.path.getsize(file.name)/1024))
			#log
			start_logging(file, serial,pi,handle)
			file.close()
		#rename file and remove the ~	
		os.rename(file_path,file_path.replace('~',''))
	#close handles
	pi.i2c_close(handle)
	pi.close()

#this stops the main function being called when the script is imported
if __name__ == "__main__":
   main()
