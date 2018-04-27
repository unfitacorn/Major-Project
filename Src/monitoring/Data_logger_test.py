import Data_logger as dl
import os.path
import pytest
import RPi.GPIO as gpio

#it will always a positive number as North/South and East/West 
def test_gps_format():
	# 5224.9671 (DDMM.MMMM) 52 + 24.9671/60
	# format will always be 8 digits
	expected = format(52 + 24.9671/60,'.5f')
	assert expected == dl.change_format_of_GPS(5224.9671)
	expected = format(00 + 00.0000/60,'.5f')
	assert expected == dl.change_format_of_GPS(0000.0000)

def test_set_up_dir():
	file = dl.set_up_dir()
	assert os.path.isfile(file)
	
def test_check_previous_file():
	file = dl.set_up_dir()
	assert os.path.isfile(file)
	dl.checkPreviousFiles()
	assert os.path.isfile(file.replace('~',''))

def test_i2c():
	i2c_bus = 1
	i2c_address = 0x5a
	pi, handle = dl.set_up_i2c(i2c_bus,i2c_address)
	air_quality_message = dl.get_air_quality_data(pi,handle)
	assert len(air_quality_message) == 9
	assert air_quality_message[2] == 0x00
	#databytes will never be negative (0 at the least)
	co2 , toc = dl.translate_air_data([0,0,0,0,0,0,0,0,0])
	assert co2 == 0
	assert toc == 0
	co2 , toc = dl.translate_air_data([99,99,99,99,99,99,99,99,99])
	assert co2 == 25443
	assert toc == 25443
	co2 , toc = dl.translate_air_data([99,0,0,0,0,0,0,5,7])
	assert co2 == 25344
	assert toc == 1287

def test_serial():
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	
	serial = dl.set_up_serial()
	assert serial.is_open
	message = dl.get_and_translate_gpgga(serial)

	assert message.get("position_fix_indicator") is '1'