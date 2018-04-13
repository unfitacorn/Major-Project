<?php
//https://www.w3schools.com/php/php_mysql_select.asp
$server = "db.dcs.aber.ac.uk";
$user = "rdm10";
$pwd = "majorproject";
$db = "rdm10";

$connection = new mysqli($server,$user,$pwd,$dbname);
if ($connection->connect_error){
	echo "<p>Connection to Aberystwyth MySQL server failed. Ensure you are connected to the university network.</p>";
}


?>