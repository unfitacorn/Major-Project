import upload as up
import pytest

#difficult to test that are tests themselves like connected(),openvpn_running() and table exists()
def test_setup_mysql():
	up.connected()
	up.openvpn_running()
	cursor_obj,connection = up.setup_mysql()
	assert connection.open

def test_create_table():
	up.connected()
	up.openvpn_running()
	cursor_obj,connection = up.setup_mysql()
	up.create_table(cursor_obj,'mmp_test')
	up.table_exists(cursor_obj,'mmp_test')
	assert True