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
	subprocess.call(['sudo','openvpn','--config','/etc/openvpn/Aberystwyth.ovpn','--daemon'])
	time.sleep(10)
	output= subprocess.run(['ifconfig', 'tun0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	if "error fetching interface" in  output:
		print("vpn error...")
		return False
	else:
		return True

def table_exists(cursor_obj):
	cursor_obj.execute("SHOW TABLES")
	tables = cursor_obj.fetchall()
	for table in tables:
		if table[0] is 'MMP':
			return True
	return False
def create_table(cursor_obj):
	sql_cmd = "CREATE TABLE MMP (timestamp INT,latitude FLOAT(4),NS_indicator char(1),longitude FLOAT(4),EW__indicator char(1),pos_fix INT,checksum CHAR(10),CO2 INT, TOC INT)"
	cursor_obj.execute(sql_cmd)
	
def setup_mysql():
	connection = pymysql.connect(host='db.dcs.aber.ac.uk',
                             user='rdm10',
                             password='majorproject',
                             db='rdm10')
	cursor_obj = connection.cursor()
	
	return cursor_obj
	
def upload(filename,cursor_obj):
	print("")

def find_and_upload_log_files(cursor_obj):
	for root, dirs,files in os.walk(os.getcwd() + '/logs'):
		for filename in files:
			if filename.startswith('log'):
				upload(filename,cursor_obj)
	
def main():
	
	if not connected() or not openvpn_running():
		print("exiting...")
		exit()
	cursor_obj = setup_mysql()
	if not table_exists(cursor_obj):
		create_table(cursor_obj)
	find_and_upload_log_files(cursor_obj)
	
	
	

main()
