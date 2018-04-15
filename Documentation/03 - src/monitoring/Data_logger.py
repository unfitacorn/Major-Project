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
"""

def led_out(flashes):
	for i in range(0,flashes):
		gpio.output(24,1)
		time.sleep(0.25)
		gpio.output(24,0)
		if flashes is not 0:
			time.sleep(0.25)


def get_and_translate_gpgga(serial):
	message = ''
	while True:
		while "GPGGA" not in message:
			message = serial.readline().decode('utf-8').replace('\r\n','')
			
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
							
		if gpgga_message.get("position_fix_indicator") is '1':
			break
		else:
			led_out(2)
			time.sleep(30)

	return gpgga_message
	
def get_air_quality_data(pi,handle):
	i2c_read_bytes = 9
	byte_when_ready = 0x00
	warm_up = True
	
	while warm_up:
		count, data = pi.i2c_read_device(handle, i2c_read_bytes)
		try:
			
			if data[2] is byte_when_ready:
				warm_up = False
			else:
				print("Air Quality Sensor in warm up state")
				led_out(3)
				time.sleep(20)
		except Exception as e:
			raise e
		
	return data

def translate_air_data(data):
	co2 = (data[0]*256)+data[1]
	toc = (data[7]*256)+data[8]
	return co2, toc

def set_up_dir():
	logs_dir = os.getcwd() + '/logs'
	if not os.path.exists(logs_dir):
		os.makedirs(logs_dir)
	file_path = logs_dir + '/~log ' + str(time.strftime("%c")) + '.txt'
	file_path = file_path.replace(':','')
	file = open(file_path,'a')
	file.write('timestamp,lat,long,pos_fix,CO2,TOC\r\n')
	file.close()
	return file_path
	
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
	print("waiting for GPS fix")
	get_and_translate_gpgga(serial_complete)
	return serial_complete
	
def set_up_i2c(i2c_bus,i2c_address):
	pi = pigpio.pi()
	if not pi.connected:
		pi.close()
		exit()
	handle = pi.i2c_open(i2c_bus, i2c_address)
	
	return pi, handle

def start_logging(file, serial,pi,handle):
	gpgga_message = get_and_translate_gpgga(serial)
	air_quality_message = get_air_quality_data(pi,handle)
	co2 , toc = translate_air_data(air_quality_message)

	if gpgga_message.get("ns_indicator") is 'S':
		gpgga_message['latitude'] = str(float(gpgga_message.get("latitude"))*-1)
	if gpgga_message.get("ew_indicator") is 'W':
		gpgga_message['longitude'] = str(float(gpgga_message.get("longitude"))*-1)

	file.write(gpgga_message.get("timestamp") + ','
				+ str(float(gpgga_message.get("latitude"))/10) + ','
				+ str(float(gpgga_message.get("longitude"))/10) + ','
				+ gpgga_message.get("position_fix_indicator") + ','
				+ str(co2) + ','
				+ str(toc) + '\r\n')
	led_out(1)


#needs to check for files that were open when RPi shuts down. Removes '~' from start of the file names
def checkPreviousFiles():
	for root, dirs,files in os.walk(os.getcwd() + '/logs'):
		for filename in files:
			if filename.startswith('~'):
				#rename file
				filenamelogs = os.getcwd() + '/logs/' + filename
				os.rename(filenamelogs,filenamelogs.replace('~',''))
		
def main():
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	print("Checking previous files")
	checkPreviousFiles()
	print("setting variables...")
	i2c_bus = 1
	i2c_address = 0x5a
	largest_file_size_kb = 25
	
	print("setting i2c interface...")
	pi, handle = set_up_i2c(i2c_bus,i2c_address)
	print("setting serial interface...")
	serial = set_up_serial()
	logging = True
	while logging:
		print("creating file...")
		file_path = set_up_dir()
		print("Logging starting...")
		while os.path.getsize(file_path)/1024 < largest_file_size_kb:
			file = open(file_path,'a')
			print("filesize: " + str(os.path.getsize(file.name)/1024))
			start_logging(file, serial,pi,handle)
			file.close()
		os.rename(file_path,file_path.replace('~',''))
	pi.i2c_close(handle)
	pi.close()

main()