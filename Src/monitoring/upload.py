#file used to upload data to sql
import socket
import subprocess
import time
import pymysql
import os

#https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python
#check connection to internet (using google)
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
#check that the vpn is running
def openvpn_running():
	#use subprocess to check if the tun0 (vpn) has been created. subprocess will run a linux command
	output= subprocess.run(['ifconfig', 'tun0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	#no output if there is an error
	#create vpn connection using abervpn
	if not output:
		print("No connection to VPN, attempting to connect")
		subprocess.call(['sudo','openvpn','--config','/etc/openvpn/Aberystwyth.ovpn','--daemon'])
		time.sleep(15)
	#run the ifconfig tun0 again
	output= subprocess.run(['ifconfig', 'tun0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	#
	if not output:
		print("Connection Failed")
		return False
	else:
		print("Connection Approved")
		return True

#check that the table exists on the mysql server
def table_exists(cursor_obj,table_name):
	cursor_obj.execute("SHOW TABLES")
	tables = cursor_obj.fetchall()
	#loop over tables checking for MMP table
	for table in tables:
		if 'MMP' in table[0]:
			return True
	return False

def create_table(cursor_obj,table_name):
	#create table if it doesn't exist
	sql_cmd = "CREATE TABLE "+table_name+ " (timestamp INT,latitude FLOAT(4),longitude FLOAT(4),pos_fix INT,CO2 INT, TOC INT)"
	cursor_obj.execute(sql_cmd)
	
def setup_mysql():
	#read file that contains unencrypted details
	file = open("sqlserverdetails.txt","r")
	#zip into dictionary
	sqldetails = dict(zip(['host','user','password','db'],file.read().splitlines()))
	#create connection using pymysql
	connection = pymysql.connect(host=sqldetails.get('host'),
                             user=sqldetails.get('user'),
                             password=sqldetails.get('password'),
                             db=sqldetails.get('db'))
	cursor_obj = connection.cursor()
	
	return cursor_obj,connection
	

def upload(filename,cursor_obj,connection):
	#open file
	file= open(filename,'r+')
	#read all lines and save in array
	data = file.read().splitlines()
	#remove headings and last line (blank line)
	data =data[1:-1]
	#create long statement for each file
	sql = "INSERT INTO MMP (timestamp,latitude,longitude,pos_fix,CO2,TOC) VALUES "
	for dataItem in data:
		if dataItem is not "":
			sql += "(" + dataItem + "),"
	#remove blank values
	sql= sql[:-1]
	cursor_obj.execute(sql)
	#commit statement
	connection.commit()

#find all log files, call upload and once the file has been uploaded -> remove the file
def find_and_upload_log_files(cursor_obj,connection):
	for root, dirs,files in os.walk(os.getcwd() + '/logs'):
		for filename in files:
			if filename.startswith('log'):
				file_location = (os.getcwd() + '/logs/'+ filename)
				upload(file_location,cursor_obj,connection)
				os.remove(file_location)
	
def main():
	#check connection
	if not connected() or not openvpn_running():
		print("exiting...")
		exit()
	#setup mysql
	cursor_obj,connection = setup_mysql()
	#create table or remove it 
	if not table_exists(cursor_obj,'MMP'):
		create_table(cursor_obj,'MMP')
	find_and_upload_log_files(cursor_obj,connection)
	print("Data Upload Complete")
if __name__ == "__main__":
	main()
