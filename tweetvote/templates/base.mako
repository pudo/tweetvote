<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>tweetvote: ${self.title()}</title>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
	<script type="text/javascript">
	
	</script>
	
	<style>
		body, td {
			font-size: 0.9em;
			font-family: 'Lucida Grande', Calibri, Helvetica, sans-serif;
		}
		body {
			background-color: #00d8ff;
		}
		
		#logo {
			margin-left: auto;
			margin-right: auto;
			padding: 1em;
			width: 347px;
		}
		
		#page_container {
			width: 444px;
			margin-left: auto;
			margin-right: auto;
		}
		
		#page {
			background-color: white;
			padding: 0 1em 0 1em;
			color: #333333;
		}
		
		#page a {
			color: #000000;
			text-decoration: none;
			font-weight: bold;
		}
		
		#footer {
			margin-left: auto;
			margin-right: auto;
			padding: 3em;
			width: 20em;
			text-align: center;
			color: white;
		}
		
		#footer a {
			text-decoration: none;
			color: white;
		}
		
		#tweet, #no_tweet {
			display: none;
		}
		
		#tweet {
			width: 100%;
		}
		
		#tweet #header {
			padding: 0.5em 0 0.7em 0;
			font-family: Georgia, serif;
			font-size: 1.8em;
			color: #bbbbbb;
		}
		
		#tweet td {
			vertical-align: top;
		}
		
		#tweet .message {
			font-size: 1.2em;
		}
		
		#tweet .time {
			font-size: 0.8em;
			color: #bbbbbb;
			text-align: right;
		}
		
		#tweet .profile_icon {
			margin: 0 0.5em 0 0;
			border: 1px solid #333333;
		}
		
		#tweet .votes {
			text-align: center;
		}
		
		#tweet .votes #vote_up {
			padding-right: 1em;
		}
		
		#tweet .votes #vote_down {
			padding-left: 1em;
		}
		
		#tweet .votes img {
			margin: 1em;
		}
		
		#please_wait {
			display: none;
			width: 444px;
			text-align: center;
			color: black;
		}
		
		.hint {
			width: 100%;
			padding: 1em;
			font-size: 0.7em;
			text-align: center;
		}
		
		strong {
			font-family: Georgia, serif;
			font-size: 2em;
			float: right;
			font-weight: normal;
			color: black;
		}
		
		.login {
			padding: 1em 0 0.3em 0;
		}
		
		.login label {
			float: left;
			width: 40%;
			margin: 0.5em 0 0 0;
		}
		
		.login input {
			margin: 0.4em 0 0 0;
			padding: 0.2em;
			display: block;
			font-size: 0.8em;
		}
		
		.login input[type=submit] {
			border: 1px solid white;
			background-color: #d4d700;
			color: white;
			font-size: 1em;
			padding: 0.3em 0.8em 0.3em 0.8em;
			margin: 0.5em;
			font-weight: bold;
		}
		
		.login .error-message {
			color: #ff5732;
		}
		
		.login br { display: none;}
		
		#searcharea {
			display: none;
			padding: 0.5em 0 2em 0;
		}
		
		#searcharea input {
			padding: 0.5em;
			font-size: 0.8em;
			min-width: 20em;
		}
		
		.working {
			background-color: #dddddd;
		}
	</style>
</head>
<body>
	<div id="logo"><img src="/logo.png" alt="tweetvote"></div>
	
	<div id="page_container">
		<img src="/page_top.png">
		<div id="page">

		${self.body()}
		</div>
		<img src="/page_bot.png">
	</div>
	
	<div id="footer">
		<a href="http://pudo.org/blog">blog</a> &middot;
		<a href="#">faq</a> &middot;
		<a href="#">api</a> &middot;
		%if 'user_id' in session: 
			<a href="/logout">end session</a> &middot;
		%endif
		<a href="http://pudo.org/blog/about/">imprint</a>
	</div>
</body>