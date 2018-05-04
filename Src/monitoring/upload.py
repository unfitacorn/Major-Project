#file used to upload data to sql
import subprocess
import time
import pymysql
import os


def connected():
    try:
        response = os.system("ping -c 1 vpn.aber.ac.uk")

        if not response:
        	return True
        else:
        	return False
    except:
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
	#run the ifconfig tun0 again. Checks if vpn is connected
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
		if table_name in table[0]:
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
	if len(data) is 0:
		return
	#create long statement for each file
	sql = "INSERT INTO MMP (timestamp,latitude,longitude,pos_fix,CO2,TOC) VALUES "
	for dataItem in data:
		if dataItem is not "":
			sql += "(" + dataItem + "),"
	#remove comma from end of string
	sql= sql[:-1]
	print("sql: " + sql)
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
