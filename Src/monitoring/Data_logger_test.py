import Data_logger as dl
import os.path
import pytest
import RPi.GPIO as gpio
import os

#it will always a positive number as North/South and East/West 
def test_gps_format():
	# 5224.9671 (DDMM.MMMM) 52 + 24.9671/60
	# format will always be 8 digits
	expected = format(52 + 24.9671/60,'.5f')
	assert expected == dl.change_format_of_GPS(5224.9671)
	expected = format(00 + 00.0000/60,'.5f')
	assert expected == dl.change_format_of_GPS(0000.0000)
#test setting up the directory
def test_set_up_dir():
	#file and directory should be created
	file = dl.set_up_dir()
	#check it exists
	result = os.path.isfile(file)
	#remove it
	os.remove(file)
	#check result before the file was removed
	assert result
	
	#test check_previous_file function
def test_check_previous_file():
	#create file
	file = dl.set_up_dir()
	#check it exists
	assert os.path.isfile(file)
	#run method
	dl.check_previous_files()
	#check filename has been replaced
	result = os.path.isfile(file.replace('~',''))
	#remove file
	os.remove(file.replace('~',''))
	#test result
	assert result
	
#test i2c functions
def test_i2c():
	#set board mode
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	#setup i2c
	pi, handle = dl.set_up_i2c()
	#get message from device
	air_quality_message = dl.get_air_quality_data(pi,handle)
	#check message length
	assert len(air_quality_message) == 9
	#check the air quality sensor is in ready mode
	assert air_quality_message[2] == 0x00
	#databytes will never be negative (0 at the least)
	#test conversion
	co2 , toc = dl.translate_air_data([0,0,0,0,0,0,0,0,0])
	assert co2 == 0
	assert toc == 0
	co2 , toc = dl.translate_air_data([99,99,99,99,99,99,99,99,99])
	assert co2 == 25443
	assert toc == 25443
	co2 , toc = dl.translate_air_data([99,0,0,0,0,0,0,5,7])
	assert co2 == 25344
	assert toc == 1287
#test UART functions
def test_serial():
	#set board mode
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	#set up serial
	serial = dl.set_up_serial()
	#check connection has been made
	assert serial.is_open
	#test if message has been recieved
	message = dl.get_and_translate_gpgga(serial)

	assert message.get("position_fix_indicator") is '1'

#test logging function
def test_start_logging():
	#create file
	file_path = dl.set_up_dir()
	#open the file - in append mode
	file = open(file_path,'a')
	#set board mode
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	#set up serial
	serial = dl.set_up_serial()
	#set up i2c
	pi, handle = dl.set_up_i2c()
	#run logging method once
	dl.start_logging(file, serial,pi,handle)
	#close file
	file.close()
	#test how many lines are written (should be 2)
	#headings and a data line
	with open(file_path) as f:
		lines = sum(1 for _ in f)
	#os.remove(file_path)
	print(file_path)
	assert 2 == lines
	