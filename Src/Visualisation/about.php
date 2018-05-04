<!--
This is used to display any errors
e.g. If permissions have not been set, an error will be stated on the webpage.
-->
<?php ini_set("display_errors", 1); ?>
<!--define the document  type-->
<!DOCTYPE html>
<html lang="en">
	<head>
		<!--Display on the window tab-->
    	<title>Air Quaity Mapping</title>
		<!--load the CSS file for this page-->
    	<link rel="stylesheet" href="index.css">

	</head>
	<body>
		<!--create links to other web pages-->
		<div id="menu">
		<ul>
  			<li><a href="index.php">Map</a></li>
  			<li><a href="about.php">About This Website</a></li>
  			<li><a href="src.php">Source and License</a></li>

		</ul>
		</div>
		<!--display info about the page with links to plugins used-->
		<div id="about">
			<h1>
				Information about this website
			</h1>
			<p>
				This page has been created for my third year major project in Aberystwyth University. 
			</p>
			<p>
				The map tiles have been provided by <a href="https://www.openstreetmap.org">OpenStreetMap</a>,  "project that creates and distributes free geographic data for the world". The overlay for the heat map uses a plugin for <a href="http://leafletjs.com/">leaflet</a>, "an open-source JavaScript for interactive maps". The overlay uses a an open-source plugin called <a href="https://github.com/Leaflet/Leaflet.heat">leaflet.heat</a>, this plugin allows for an easy creation of heat maps using latitude and longitutde co-ordinates along with an intensity value. This project would not be possible without OpenStreetMap, Leaflet and leaflet.heat.
			</p>
			<p>
				Data is collected using a microcontroller, GPS and air quality sensor. The data has been collected in a vehicle as they are often used for long distances and can collect a large amount fo data.
			</p>
			<h1>
				How to use the source
			</h1>
				<ul>
					<li>Download the source code from the source tab.</li>
					<li>Edit the getData.php file to link to the database.</li>
					<li>Edit the same file to query the required database.</li>
					<li>Ensure the server you are hosting on can use php.</li>
					<li>Edit php pages to fit your needs.</li>
				</ul>
				
		</div>
		<br>
		<!-- This footer is on each webpage -->
		<div id="footer">
		<p>
			The information provided on this and other pages by me, Robert Mouncer (rdm10@aber.ac.uk), is under my own personal responsibility and not that of Aberystwyth University. Similarly, any opinions expressed are my own and are in no way to be taken as those of A.U. The use of the University's logo or crest is not allowed on individual user's web pages.
		</p>
		<!--validators for easy development-->
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
