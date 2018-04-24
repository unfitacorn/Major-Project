
import RPi.GPIO as gpio
import time
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
		time.sleep(0.25)


def main():
	gpio.setmode(gpio.BCM)
	gpio.setup(24,gpio.OUT)
	led_out(5)

main()