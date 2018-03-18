import socket
import subprocess
import time
import pymysql

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
	if "error fetching interface" in  output:
		print("vpn error...")
		return False
	else:
		return True

def db_exists(cursor_obj):
	cursor_obj.execute("show tables")
	rows = cursor_obj.fetchall()
	print(rows)
	return False
	
def setup_mysql():
	connection = pymysql.connect(host='db.dcs.aber.ac.uk',
                             user='rdm10',
                             password='majorproject',
                             db='rdm10')
	cursor_obj = connection.cursor()
	if db_exists(cursor_obj):
		print("")
	return
							 
	
	
def main():
	time.sleep(10)
	if not connected() or not openvpn_running():
		print("exiting...")
		exit()
	setup_mysql()
	print("done")

main()
