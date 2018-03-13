import pigpio
import time

def get_air_quality_data(pi,handle):
	i2c_read_bytes = 9
	
	warm_up = True
	while warm_up:
		
		count, data = pi.i2c_read_device(handle, i2c_read_bytes)
		
		print(data[2])
		if data[2] is 0x00:
			warm_up = False
		
	
	return data

def setup_i2c(i2c_bus,i2c_address):
	pi = pigpio.pi()
	if not pi.connected:
		print("no pi")
	handle = pi.i2c_open(i2c_bus, i2c_address)
	
	return pi, handle
	
	

i2c_bus = 1
i2c_address = 0x5a
pi, handle = setup_i2c(i2c_bus,i2c_address)
while True:
	data = get_air_quality_data(pi,handle)
	time.sleep(1)

pi.i2c_close(handle)
pi.close()