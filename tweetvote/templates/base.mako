<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>tweetvote: ${self.title()}</title>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
	<script type="text/javascript" src="/script.js"></script>
	<link rel="stylesheet" type="text/css" href="/style.css" />
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
		<a href="http://github.com/pudo/tweetvote/blob/727a44b90a7b29c41fc546ec14b9a3336adc34ab/tweetvote/controllers/votes.py">api</a> &middot;
		<a href="http://pudo.org/blog/about/">imprint</a>
	</div>
</body>