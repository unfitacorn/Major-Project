TITLE: AIR QUALITY MAPPING
MARK ACHIEVED: 74
#################################Documentation##################################
01 - Planning
	All documents related to planning including the OPS included in this folder
02 - Design
	All documents related to Design. These include diagrams, images and datasheets
03 - Report
	Final report has been stored here.
99 - presentations
	Presentations given in supervisor meetings are stored here.

#################################Src##################################
______Monitoring______
The monitoring system is for collceting data using a GPS and air quality sensor. Data is gathered and then uploaded to the University MySQL server before being removed from the device.
Monitoring files are designed and implemented to work with a Raspberry Pi Model 3B+ (RPI) with specific components running on Raspbian Lite. These scripts will most likely fail without the hardware connected and correct configuration.
GPS - PModGPS GPS receiver: https://uk.rs-online.com/web/p/processor-microcontroller-development-kits/1346455/
Air quality Sensor:ams IAQ-CORE P- https://uk.rs-online.com/web/p/colour-light-sensors/1730309/

Crontab jobs should be created using 'crontab -e'. This should be appeneded to the end of the file:

	@reboot sleep 20 && /home/pi/startlogger.sh
	* /2 * * * * /home/pi/runUpload.sh

This will run data logging python script on start up and the uploader every 2 minutes.

Required setup:
	The following packages need installing on the RPI:
		- openvpn (sudo apt-get install openvpn)
		- serial (sudo apt-get install python-serial)
		- pigpio (http://abyz.me.uk/rpi/pigpio/download.html)
		- pytest (pip install -U pytest)
		- pymysql (pip install PyMySQL)

	All Python files are designed to run on Python3. The following files and folder should be in the user directory of the RPI (/home/pi/):
		- /logs/ (example log contained in this folder)
		- Data_logger.py (collects data from the GPS and air quality sensor and logs them in the /logs/ folder)
		- Data_logger_test.py (unit tests for the Data_logger.py)
		- runTests.sh (Will run both unit test files Data_logger_test.py and upload_test.py)
		- runUpload.sh (Run the upload script and kill any OpenVPN instances)
		- sqlserverdetails.txt (this should be configured, removing the current tags and replacing it with the correct configuration for the MySQL server)
		- startlogger.sh (starts pigpiod and runs the Data_logger.py script)
		- upload.py (Uploads data from the /logs/ directory to the MySQL server)
		- upload_test.py (unit tests for the upload.py script)

	The following files need to be moved to the openvpn directory (/etc/openvpn/):
		- Aberystwyth.ovpn (configuration file with openvpn keys to connect to the Aberystwyth University VPN)
		- pass.txt (replace tags with userid and password)

______Visualisation______
The visualisation application uses data collected from the monitoring system to create a visualisation tool for air quality.
This must run on a web hosting server with PHP installed. This must be hosted on the university network as access is required to the MySQL server.
The map is powered by a OpenStreetMap library called Leaflet.
To see the site running - visit users.aber.ac.uk/rdm10/visualisation
No additional packages need installing
Required setup:
	The following files and folders must retain the directory format:
		- /dist/
			- leaflet-heat.js (intensity not using rolling average. bugs present)
			- leaflet-heat1.js (fixed intensity issue as mentioned in report. Still bugs present)
		- /images/ (images for leaflet plugin)
		- about.php (html file for the about page)
		- getData.php (Retrieves data from MySQL server)
		- index.css (CSS for each webpage)
		- index.php (home page of website with interactive map)
		- leaflet.css (css for leaflet)
		- leaflet.js (leaflet file)
		- leaflet.js.map (leaflet file)
		- leaflet-src.js (leaflet file)
		- leaflet-src.js.map (leaflet file)
		- LICENSE.txt (license of visualisation tool)
		- Source.zip (zip for source download)
		- src.php (html file for source page)
		
	

