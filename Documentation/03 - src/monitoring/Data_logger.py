import serial
import time
import RPi.GPIO as gpio
import os
import pigpio



def get_and_translate_gpgga(serial):
	message = ''
	while "GPGGA" not in message:
		message = serial.readline().decode('utf-8')
			
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
	return gpgga_message
	
def get_air_quality_data():
	pi = pigpio.pi()
	if not pi.connected:
		print("no pi")
	i2c_bus = 1
	i2c_address = 0x5a
	i2c_read_bytes = 9
	
	warm_up = True
	while warm_up:
		handle = pi.i2c_open(i2c_bus, i2c_address)
		count, data = pi.i2c_read_device(handle, i2c_read_bytes)
		
		print(data[2])
		if data[2] is 0x00:
			warm_up = False
		
	#pi.i2c_close(handle)
	#pi.stop()
	return data

def translate_air_data(data):
	co2 = (data[0]*256)+data[1]
	toc = (data[7]*256)+data[8]
	return co2, toc

def set_up_dir():
	logs_dir = os.getcwd() + '/logs'
	if not os.path.exists(logs_dir):
		os.makedirs(logs_dir)
	file_path = logs_dir + '/log ' + str(time.strftime("%c")) + '.txt'
	file_path = file_path.replace(':','')
	file = open(file_path,'a')
	file.write('timestamp,lat,ns,long,ew,pos_fix,checksum,CO2,TOC\r\n')
	return file
	
def set_up_serial():
	gpio.setmode(gpio.BCM)
	gpio.setup(12,gpio.OUT)
	serial_complete = serial.Serial(
			   port='/dev/ttyS0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
	)
	return serial_complete
	
def start_logging(file, serial):
	while True:
		gpgga_message = get_and_translate_gpgga(serial)

		co2 , toc = translate_air_data(air_quality_message)
		file.write(gpgga_message.get("timestamp") + ','
				   + gpgga_message.get("latitude") + ','
				   +gpgga_message.get("ns_indicator") + ','
				   +gpgga_message.get("longitude") + ','
				   +gpgga_message.get("ew_indicator") + ','
				   +gpgga_message.get("position_fix_indicator") + ','
				   +gpgga_message.get("checksum") + ','
				   + co2 + ','
				   + toc)
		print(file.name)
		
def main():
	serial = set_up_serial()
	file = set_up_dir()
	start_logging(file, serial)
	#file.close()
	
air_quality_message = get_air_quality_data()
main()