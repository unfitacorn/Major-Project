import socket
import subprocess
import time
import pymysql
import os

#https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python
def connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
def openvpn_running():
	output= subprocess.run(['ifconfig', 'tun0'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	if not output:
		print("No connection to VPN, attempting to connect")
		subprocess.call(['sudo','openvpn','--config','/etc/openvpn/Aberystwyth.ovpn','--daemon'])
		time.sleep(15)

	output= subprocess.run(['ifconfig', 'tun0'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	if not output:
		print("Connection Failed")
		return False
	else:
		print("Connection Approved")
		return True

def table_exists(cursor_obj):
	cursor_obj.execute("SHOW TABLES")
	tables = cursor_obj.fetchall()
	for table in tables:
		if 'MMP' in table[0]:
			return True
	return False
	
def create_table(cursor_obj):
	sql_cmd = "CREATE TABLE MMP (timestamp INT,latitude FLOAT(4),longitude FLOAT(4),pos_fix INT,CO2 INT, TOC INT)"
	cursor_obj.execute(sql_cmd)
	
def setup_mysql():
	file = open("sqlserverdetails.txt","r")
	sqldetails = dict(zip(['host','user','password','db'],file.read().splitlines()))
	connection = pymysql.connect(host=sqldetails.get('host'),
                             user=sqldetails.get('user'),
                             password=sqldetails.get('password'),
                             db=sqldetails.get('db'))
	cursor_obj = connection.cursor()
	
	return cursor_obj,connection
	
def upload(filename,cursor_obj,connection):
	file= open(filename,'r+')
	data = file.read().splitlines()
	print(data[1:-1])
	data =data[1:-1]
	
	sql = "INSERT INTO MMP (timestamp,latitude,longitude,pos_fix,CO2,TOC) VALUES "
	for dataItem in data:
		if dataItem is not "":
			sql += "(" + dataItem + "),"


		
	sql= sql[:-1]
	cursor_obj.execute(sql)
	connection.commit()


def find_and_upload_log_files(cursor_obj,connection):
	for root, dirs,files in os.walk(os.getcwd() + '/logs'):
		for filename in files:
			if filename.startswith('log'):
				file_location = (os.getcwd() + '/logs/'+ filename)
				upload(file_location,cursor_obj,connection)
				os.remove(file_location)
	
def main():
	
	if not connected() or not openvpn_running():
		print("exiting...")
		exit()
	cursor_obj,connection = setup_mysql()
	if not table_exists(cursor_obj):
		create_table(cursor_obj)
	find_and_upload_log_files(cursor_obj,connection)
	
	
	

main()
