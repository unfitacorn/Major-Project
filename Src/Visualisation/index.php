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
    	<!--Leaflet stylesheet needed for map support-->
    	<link rel="stylesheet" href="leaflet.css" />
    	<!--load the CSS file for this page-->
    	<link rel="stylesheet" href="index.css">
    	<!--load the script to support the map-->
    	<script src="leaflet.js"></script>
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
		<!-- Short instruction on how to use click function -->
		<div id="click">
			<p>Click the map locaiton to find out information about your local area</p>
		</div>
		<!--div placeholder for map imported using leaflet-->
		<div id="map"></div>
		
		<!--
		Change value for different implementations
		<script src="./dist/leaflet-heat.js"></script>
		can be used for old implementation
		-->
		<script src="./dist/leaflet-heat1.js"></script>

		<!-- Two placeholders for information given on click -->
		<div id="value_air_quality"></div>
		<div id="additional_info"></div>
		<!-- form for radio button-->
		<form id="radios">
			<!--
			label is linked to the input to ease CSS
			default checked radio button is co2.
			when a radio button is pressed, changeData() is called
			-->
			<label for="data_type_CO2">CO2 (parts per million)</label>
  			<input type="radio" name="data_type" id="data_type_CO2" value="CO2" checked="checked" onchange="changeData()">
  				
  			<label for="data_type_TOC">TVOC (parts per Billion)</label>
  			<input type="radio" name="data_type" id="data_type_TOC" value="TOC" onchange="changeData()">
		</form>
  		<form id="ranges">
  			<!-- http://form.guide/html-form/html5-input-type-range.html -->

  			<!--
			label is linked to the input to ease CSS
			output tag is to display the current value of the sliders
			On change the function changeData() will be called
			-->
  			<label for="maximum_range_id">Maximum intensity</label>
  			<input type="range" name="maximum_range" id="maximum_range_id" value="1000" min="0" max="5000" onchange="changeData()" oninput="maximum_point_dig.value = maximum_range_id.value">
   			<output  id="maximum_point_dig"></output>

   			<label for="radius_id">Radius of Points (Not implemented)</label>
  			<input type="range" name="radius" id="radius_id" value="25" min="0" max="50" onchange="changeData()" oninput="radius_dig.value = radius_id.value">
   			<output  id="radius_dig"></output>

   			<label for="blur_id">Blur of Points (Not implemented)</label>
  			<input type="range" name="blur" id="blur_id" value="15" min="0" max="50" onchange="changeData()" oninput="blur_dig.value = blur_id.value">
   			<output  id="blur_dig"></output>

   			<label for="minOpacity_id">Minimum Opacity of Points</label>
  			<input type="range" name="minOpacity" id="minOpacity_id" value="0.05" step="0.05" min="0" max="1" onchange="changeData()" oninput="minOpacity_dig.value = minOpacity_id.value">
   			<output  id="minOpacity_dig"></output>
   				

		</form>
		<!--Retrieve data from the sql server by calling php function-->
		<?php include  'getData.php';?>
		<script>
			//function to update the visible data 
			function changeData(){
				//find out value of radio button and splice the array to suit the needs of the heat map
				getCO2orTOC();
				//get values from slider
				var max_value = document.getElementById("maximum_range_id").value;
				var radius_value = document.getElementById("radius_id").value;
				var blur_value = document.getElementById("blur_id").value;
				var minOpacity_value = document.getElementById("minOpacity_id").value;
				//remove the current heat map and redraw it
				heat.remove();
				heat=L.heatLayer(data,{}).addTo(map);	
				//add options to heatmap - some variables are missing due to bugs	
				heat.setOptions({max:max_value, minOpacity:minOpacity_value});

			}
			//splice array depending on which radio button is pressed.
			function getCO2orTOC(){
				//restore data back to the original dataset
				data = databack.map(function(arr) {return arr.slice();});
				//find out which button is pressed
				var radioButton = document.querySelector('input[name = "data_type"]:checked').value;

				//splice array depending on radio button
				if (radioButton == 'TOC'){
					for( const array of data){
							array.splice(2, 1);
					}

				}else{
					for( const array of data){
							array.splice(3, 1);
					}

				}
			}
			//https://gis.stackexchange.com/questions/39055/how-to-get-the-lat-long-of-a-clicked-location-using-leaflet-api
			//stumbled across this when looking up how to get lat long co-ords. Altered to fit the requirements.

			// Convert Degress to Radians
			//this function is not my work
			function Deg2Rad(deg) {
					return deg * Math.PI / 180;
			}
			//pythagoas function to word out distance between two points.
			//this function is not my work, it has been adapted
			function PythagorasEquirectangular(lat1, lon1, lat2, lon2) {
					lat1 = Deg2Rad(lat1);
					lat2 = Deg2Rad(lat2);
					lon1 = Deg2Rad(lon1);
					lon2 = Deg2Rad(lon2);
					var R = 6371; // km
			  	var x = (lon2 - lon1) * Math.cos((lat1 + lat2) / 2);
			  	var y = (lat2 - lat1);
			  	var d = Math.sqrt(x * x + y * y) * R;
			  	return d;
			}

			// compare distnaces between points will find the closest point, if within the mindif minimum difference
			//this function is not my work, it had been adapted
			function NearestPoint(latitude, longitude) {
				var mindif = 0.5;
				var found = false;
				var closest;

				getCO2orTOC();
				for (index = 0; index < data.length; ++index){
					var dif = PythagorasEquirectangular(latitude, longitude, data[index][0], data[index][1]);
					if (dif < mindif) {
	  					closest = index;
	  					mindif = dif;
						found = true;
					}
				}
					
					//get current radio button value - co2 or toc
					var radioButtonValue = document.querySelector('input[name = "data_type"]:checked').value;
				//if value was found, display it otherwise no data
				if (found == true){
					document.getElementById("value_air_quality").innerHTML = radioButtonValue + ": " + data[closest][2];
				} else {
					document.getElementById("value_air_quality").innerHTML = radioButtonValue + ": No data";
				}
					
					document.getElementById("additional_info").innerHTML = "Insert information here about effects on human health"
			}
					
		</script>

		<script>
		//run this script when the page first starts
			//splice array to co2 values
			for( const array of data){
							array.splice(2, 1);
					}
			//create map object set to view aberystwyth
			var map = L.map('map').setView([52.4147, -4.0842], 12);
			//create map tiles from openstreetmap
			var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
			    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
			}).addTo(map);
			//create heat layer for heat map
			var heat = L.heatLayer(data,{}).addTo(map);
			//if the map is clicked on - run the nearest point function
			map.on('click', function(e) {NearestPoint(e.latlng.lat,e.latlng.lng)});
			//update the data
			changeData();
		</script>
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
