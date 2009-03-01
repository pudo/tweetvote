<%inherit file="base.mako" />
<%def name="title()">Welcome</%def>
<a href="http://twitter.com">twitter</a> asked millions one question: <br>
<strong>what are you doing?</strong>
<div style="clear: both;"></div>
<br>
<br>
<b>tweetvote</b> asks a new question: <br>
<strong>do you give a shit?</strong>
<div style="clear: both;"></div>
<br>
<br><br>
On tweetvote, you rate tweets. Over time, this will allow us to <b>create message 
filters</b> that can adapt to your interests, give you the <b>tweets you want to see</b>, 
while <b>hiding the chitchat</b> you really don't care about. 
<br><br>
<strong>snob in</strong>
<div style="clear: both;"></div>
<form class="login" name="login" method="post" action="/login">
	<label for="username">Twitter Username:</label>
	<input name="username" type="text" />

	<label for="password">Password:</label>
	<input type="password" name="password">
	
	<label for="submit">&nbsp;</label>
	<input name="submit" type="submit" class="submit" value="Login"/>
</form>
<div style="clear: both;"></div>

<div class="hint">
Your password will never be saved on our 
servers and is only used to identify you and to communicate with Twitter.

Once Twitter has finished OAuth support, we'll offer a more secure 
method to log into tweetvote. 
</div>