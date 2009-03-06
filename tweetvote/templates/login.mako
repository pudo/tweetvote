<%inherit file="base.mako" />
<%def name="title()">Welcome</%def>
<div class="loginpage">
	<a href="http://twitter.com">twitter</a> asked millions one question:
	<strong>what are you doing?</strong>
	
	<b>tweetvote</b> asks a new question:
	<strong>do you give a shit?</strong>
	
	On tweetvote, you rate tweets. Over time, this will allow us to <b>create message 
	filters</b> that can adapt to your interests, give you the <b>tweets you want to see</b>, 
	while <b>hiding the chitchat</b> you really do not care about. 
	<br>
	<strong>snob in</strong>
	Ok, time for the login. We need this to load <b>your timeline</b>.
	<form class="login" name="login" method="post" action="/login">
		<label for="username">Twitter Username:</label>
		<input name="username" type="text" />

		<label for="password">Password:</label>
		<input type="password" name="password">
	
		<label for="submit">&nbsp;</label>
		<input name="submit" type="submit" class="submit" value="Login"/>
	</form>
	<strong>how to</strong>
	As we all know, computers are controlled with <b>a keyboard</b>. Here is how:
	<center><img src="/keys.png" /></center>
	<!--
	<b>Rate</b> as many tweets as you can so <b>tweetvotes recommendations</b> will improve. 
	-->
	<div class="hint">
	Your password will never be saved on our 
	servers and is only used to identify you and to communicate with Twitter.

	Once Twitter has finished OAuth support, we'll offer a more secure 
	method to log into tweetvote. 
	</div>
</div>