import serial
import time
import RPi.GPIO as gpio
import os


def getAndTranslateGPGGA(serial):
	message = ''
	while ("GPGGA" not in message):
		message = serial.readline().decode('utf-8')
			
	GPGGAMessage = dict(zip(["message_ID",
						"timestamp",
						"latitude",
						"ns_indicator",
						"longitude",
						"ew_indicator",
						"position_fix_indicator",
						"satelites_used",
						"HDOP",
						"msl_altitude",
						"units",
						"geoal_seperation",
						"units",
						"age_of_diff_corr",
						"checksum"],message.split(",")))
	return GPGGAMessage
	
	
def setUpDir():
	logsDir = os.getcwd() + '/logs'
	if not os.path.exists(logsDir):
		os.makedirs(logsDir)
	filepath = logsDir + '/log ' + str(time.strftime("%c")) + '.txt'
	filepath = filepath.replace(':','')
	file = open(filepath,'a')
	file.write('timestamp,lat,ns,long,ew,pos_fix,checksum\r\n')
	return file
	
def setUpSerial():
	gpio.setmode(gpio.BCM)
	gpio.setup(12,gpio.OUT)
	serialComplete = serial.Serial(
			   port='/dev/ttyS0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
	)
	return serialComplete
	
def startlogging(file, serial):
	while True:
			mess = getAndTranslateGPGGA(serial)
			file.write(mess.get("timestamp") + ',' + mess.get("latitude") + ',' +mess.get("ns_indicator") + ',' +mess.get("longitude") + ',' +mess.get("ew_indicator") + ',' +mess.get("position_fix_indicator") + ',' +mess.get("checksum") )
			print(file.name)
def main():
	serial = setUpSerial()
	file = setUpDir()
	startlogging(file, serial)
	
		
main()