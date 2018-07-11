import upload as up
import pytest

#difficult to test that are tests themselves like connected(),openvpn_running() and table exists()
#test conncetion to mysql server
def test_setup_mysql():
	#check internet connection
	up.connected()
	#run vpn
	up.openvpn_running()
	#create connection object
	cursor_obj,connection = up.setup_mysql()
	#test object connection is open
	assert connection.open
#create table and check it exists
def test_create_table():
	#check vpn is running
	up.connected()
	up.openvpn_running()
	#create table
	table_name = 'mmp_test'
	cursor_obj,connection = up.setup_mysql()
	up.create_table(cursor_obj,table_name)
	#check table exists
	result = up.table_exists(cursor_obj,table_name)
	#drop the table
	sql = 'DROP TABLE ' + table_name + ';'
	cursor_obj.execute(sql)
	#test result
	assert result
	#check if table exists which it shouldn't
	result = up.table_exists(cursor_obj,table_name)
	assert not result
#test internet conncetion
def test_connected():
	assert up.connected()
#test vpn is running
def test_openvpn_running():
	assert up.openvpn_running()
#for test when internet is unplugged
def test_not_connected():
	assert not up.connected()
#for test when internet is unplugged
def test_not_openvpn_running():
	assert not up.openvpn_running()
