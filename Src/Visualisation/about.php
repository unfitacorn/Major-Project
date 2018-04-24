<?php ini_set("display_errors", 1); ?>
<!DOCTYPE html>
<html lang="en">
	<head>
    	<title>test</title>

    	<link rel="stylesheet" href="index.css">

	</head>
	<body>
		<div id="menu">
		<ul>
   			<li><a href="/rdm10/visualisation/">Map</a></li>
  			<li><a href="/rdm10/visualisation/about.php">About This Website</a></li>
  			<li><a href="/rdm10/visualisation/src.php">Source and License</a></li>

		</ul>
		</div>
		
		<div id="about">
			<p>
				This page has been created for my third year major project in Aberystwyth University. 
			</p>
			<p>
				The map tiles have been provided by <a href="https://www.openstreetmap.org">OpenStreetMap</a>,  "project that creates and distributes free geographic data for the world". The overlay for the heat map uses a plugin for <a href="http://leafletjs.com/">leaflet</a>, "an open-source JavaScript for interactive maps". The overlay uses a an open-source plugin called <a href="https://github.com/Leaflet/Leaflet.heat">leaflet.heat</a>, this plugin allows for an easy creation of heat maps using latitude and longitutde co-ordinates along with an intensity value. This project would not be possible without OpenStreetMap, Leaflet and leaflet.heat.
			</p>
			<p>
				Data is collected using a microcontroller, GPS and air quality sensor. The data has been collected in a vehicle as they are often used for long distances and can collect a large amount fo data.
			</p>
		</div>
		</br>
		<div id="footer">
		<p>
			The information provided on this and other pages by me, Robert Mouncer (rdm10@aber.ac.uk), is under my own personal responsibility and not that of Aberystwyth University. Similarly, any opinions expressed are my own and are in no way to be taken as those of A.U. The use of the University's logo or crest is not allowed on individual user's web pages.
		</p>

		<p>
      		<a href="http://validator.w3.org/check?uri=referer"><img
			src="http://www.w3.org/html/logo/badge/html5-badge-h-solo.png" 
			width="63" height="64" alt="Valid HTML5!" /></a>
			
 			<a href="http://jigsaw.w3.org/css-validator/check/referer">
 			<img style="border:0;width:88px;height:31px"
       		src="http://jigsaw.w3.org/css-validator/images/vcss" 
       		alt="Valid CSS!" /></a>
		</p>
		</div>
	</body>
</html>
