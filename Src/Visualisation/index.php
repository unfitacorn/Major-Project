<?php ini_set("display_errors", 1); ?>
<!DOCTYPE html>
<html lang="en">
	<head>
    	<title>test</title>
    	<link rel="stylesheet" href="leaflet.css" />

    	<link rel="stylesheet" href="index.css">

    	<script src="leaflet.js"></script>
	</head>
	<body>
		<div id="menu">
		<ul>
  			<li><a href="/rdm10/visualisation/">Map</a></li>
  			<li><a href="/rdm10/visualisation/about.php">About This Website</a></li>
  			<li><a href="/rdm10/visualisation/src.php">Source and License</a></li>

		</ul>
		</div>

		<br>

		<div id="map"></div>
			<script src="./dist/leaflet-heat1.js"></script>
			<div id="value_air_quality"></div>
			<div id="additional_info"></div>
			<form id="radios">

				<label for="data_type_CO2">CO2 (parts per million)</label>
  				<input type="radio" name="data_type" id="data_type_CO2" value="CO2" checked="checked" onchange="changeData()">
  				
  				<label for="data_type_TOC">TO2 (parts per million)</label>
  				<input type="radio" name="data_type" id="data_type_TOC" value="TOC" onchange="changeData()">
			</form>
  			<form id="ranges">
  				<!-- http://form.guide/html-form/html5-input-type-range.html -->
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
			<div id="test"></div>
			
			
			<?php include  'getData.php';?>
			<script>
				function changeData(){
					getCO2orTOC();
					var max_value = document.getElementById("maximum_range_id").value;
					var radius_value = document.getElementById("radius_id").value;
					var blur_value = document.getElementById("blur_id").value;
					var minOpacity_value = document.getElementById("minOpacity_id").value;

					heat.remove();
					heat=L.heatLayer(data,{}).addTo(map);		
					heat.setOptions({max:max_value, minOpacity:minOpacity_value});

				}
				function getCO2orTOC(){
					data = databack.map(function(arr) {return arr.slice();});

					var radioButton = document.querySelector('input[name = "data_type"]:checked').value;
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
				function Deg2Rad(deg) {
  					return deg * Math.PI / 180;
				}
  				
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

				function NearestPoint(latitude, longitude) {
  					var mindif = 0.5;
  					var closest;

  					getCO2orTOC();
  					for (index = 0; index < data.length; ++index){
  						var dif = PythagorasEquirectangular(latitude, longitude, data[index][0], data[index][1]);
    					if (dif < mindif) {
      						closest = index;
      						mindif = dif;
    					}
  					}
  					var radioButtonValue = document.querySelector('input[name = "data_type"]:checked').value;
  					document.getElementById("value_air_quality").innerHTML = radioButtonValue + ": " + data[closest][2];
  					document.getElementById("additional_info").innerHTML = "Insert information here about effects on human health"
				}
					
			</script>
			<script>
				for( const array of data){
   							array.splice(3, 1);
						}

				var map = L.map('map').setView([52.4147, -4.0842], 12);

				var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
				    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
				}).addTo(map);

				var heat = L.heatLayer(data,{}).addTo(map);

				map.on('click', function(e) {NearestPoint(e.latlng.lat,e.latlng.lng)});

				changeData();
			</script>
			
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
