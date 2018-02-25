import serial
import time
import RPi.GPIO as gpio
import os


def getAndTranslateGPGGA():
	waitforGPGGAmessage = True
	while True:
		message = serial.readline().decode('utf-8')
		if "GPGGA" in message:
			waitforGPGGAmessage = False
	
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
	
	
#MAIN
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

serial = setUpSerial()
logsDir = os.getcwd() + '/logs'
if not os.path.exists(logsDir):
    os.makedirs(logsDir)
fpath = logsDir + '/log ' + str(time.strftime("%c")) + '.txt'
fpath = fpath.replace(':','')
f = open(fpath,'a')
f.write('timestamp,lat,ns,long,ew,pos_fix,checksum\r\n')


while True:
	mess = getAndTranslateGPGGA()
	f.write(mess.get("timestamp") + ',' + mess.get("latitude") + ',' +mess.get("ns_indicator") + ',' +mess.get("longitude") + ',' +mess.get("ew_indicator") + ',' +mess.get("position_fix_indicator") + ',' +mess.get("checksum") )
