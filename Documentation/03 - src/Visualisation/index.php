
<!DOCTYPE html>
<html>
	<head>
    	<title>test</title>
    	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.css" />
    	<script src="http://cdn.leafletjs.com/leaflet/v0.7.7/leaflet.js"></script>
    	<style>
        	#map { width: 800px; height: 600px; }
    	</style>
	</head>
	<body>
		<div id="map"></div>
			<script src="./dist/leaflet-heat.js"></script>

			

			<script>

				var map = L.map('map').setView([52.4147, -4.0842], 12);

				var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
				    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
				}).addTo(map);

				data = data.map(function (p) { return [p[0], p[1]]; });

				var heat = L.heatLayer(addressPoints).addTo(map);

			</script>
			<?php
				include  'getData.php';
			?>
	</body>
</html>
