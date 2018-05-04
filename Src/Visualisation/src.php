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
		<!--create download links-->
		<div id="downloads">
			<ul>

				<li><a href="Source.zip" download>Source</a></li>
				<li><a href="LICENSE.txt" download>License</a></li>
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
