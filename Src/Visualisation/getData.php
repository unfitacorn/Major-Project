<?php
//displays php errors on the webpage its executed
ini_set("display_errors", 1);

//https://www.w3schools.com/php/php_mysql_select.asp
//insert server details here (password has been removed)
$server = "db.dcs.aber.ac.uk";
$user = "rdm10";
$pwd = "";
$db = "rdm10";
//create connection object to the server
$connection = new PDO("mysql:host=$server;dbname=$db", $user,$pwd);
//sql query to be executed on the server
$sqlQuery = "SELECT latitude,longitude,CO2,TOC FROM MMP;";
//hold the result of the query
$result=$connection->query($sqlQuery)->fetchAll(PDO::FETCH_NUM);
//create variable in javascript
echo "<script>";
//data = result in 2d array
echo "var data =". json_encode($result). ";";
//create copy of data that is used when data needs to be respliced
echo "var databack = data.map(function(arr) {return arr.slice();});";
//end script
echo "</script>";
?>
