<?php
ini_set("display_errors", 1);

//https://www.w3schools.com/php/php_mysql_select.asp
$server = "db.dcs.aber.ac.uk";
$user = "rdm10";
$pwd = "majorproject";
$db = "rdm10";

$connection = new PDO("mysql:host=$server;dbname=$db", $user,$pwd);

$sqlQuery = "SELECT latitude,longitude,CO2,TOC FROM MMP;";

$result=$connection->query($sqlQuery)->fetchAll(PDO::FETCH_NUM);

echo "<script>";
echo "var data =". json_encode($result). ";";
echo "var databack = data.map(function(arr) {return arr.slice();});";
echo "</script>";
?>
