<%inherit file="base.mako" />
<%def name="title()">Advanced Programming Interface</%def>
<div class="loginpage">
	<strong>tweetvote api</strong>
	
	<b>tweetvote</b> is a very simple, RESTful web application that can be used directly via its 
	HTML interface or by way of any REST-enabled application, such as a Twitter client with voting
	capabilities. 
	<br><br>
	
	<b>tweetvote</b> exposes a REST resource, <code>votes</code>. A new <code>vote</code> can be created 
	by executing a POST at <code>/votes</code>. The newly created resource will be assigned an <code>id</code>
	which can then be used to access, modify or delete the resource at <code>/votes/<i>id</i></code>. <br>
	Some actions <b>require authentication</b>. Authentication is performed via <code>HTTP Basic</code> request 
	headers, which will be directly forwarded to Twitter and checked there. Once Twitter makes <code>OAuth</code>
	tokens publicly available, those will be available as an alternative means of identifying users. 
	<br><br>
	
	<strong>actions</strong>
	<b>list</b><br>
	URL: <code>http://tweetvote.infofaktur.de/votes[.format]</code><br>
	Method: <code>GET</code><br>
	Formats: <code>json, xml</code><br>
	Requires authentication: No<br><br>
	Returns a list of items (in the specified format) or a system message.<br><br>
	Request parameters:
	<ul>
		<li><code>vote_user</code>: Twitter user ID or user name of the voting user.</li>
		<li><code>tweet_user</code>: Twitter user ID or user name of the author of the tweet that has been 
		voted on.</li>
		<li><code>status</code>: Status ID to find votes for.</li>
		<li><code>count</code>: Number of items per page.</li>
		<li><code>page</code>: Page number.</li>
	</ul>
	
	
	<b>create</b><br>
	URL: <code>http://tweetvote.infofaktur.de/votes[.format]</code><br>
	Method: <code>POST</code><br>
	Formats: <code>json, xml, html</code><br>
	Requires authentication: Yes<br><br>
	The input type will be determined based on the <code>Content-Type</code> header of the request. Valid types 
	are <code>text/javascript</code> for JSON content or <code>text/xml</code> for XML submissions. All other 
	values will be treated as <code>application/x-www-form-urlencoded</code>, i.e. common POST forms. The created
	entity (in the specified format) or a system message will be returned.<br><br>
	Expected request fields:
	<ul>
		<li><code>tweet_id</code>: Status ID to vote on.</li>
		<li><code>weight</code>: A floating point to describe the weight of the vote; subzero will be interpreted 
		as a downvote.</li>
	</ul>
	
	<b>view</b><br>
	URL: <code>http://tweetvote.infofaktur.de/votes/<i>id</i>[.format]</code><br>
	Method: <code>GET</code><br>
	Formats: <code>json, xml, html</code><br>
	Requires authentication: No<br><br>
	Returns an item (in the specified format) or a system message.
	<br><br>
	
	<b>update</b><br>
	URL: <code>http://tweetvote.infofaktur.de/votes/<i>id</i>[.format]</code><br>
	Method: <code>POST</code>, <code>PUT</code><br>
	Formats: <code>json, xml, html</code><br>
	Requires authentication: Yes<br><br>
	The input type will be determined based on the <code>Content-Type</code> header of the request. Valid types 
	are <code>text/javascript</code> for JSON content or <code>text/xml</code> for XML submissions. All other 
	values will be treated as <code>application/x-www-form-urlencoded</code>, i.e. common POST forms. The updated
	entity (in the specified format) or a system message will be returned.<br><br>
	Expected request fields:
	<ul>
		<li><code>weight</code>: A floating point to describe the weight of the vote; subzero will be interpreted 
		as a downvote.</li>
	</ul>
	
	<b>delete</b><br>
	URL: <code>http://tweetvote.infofaktur.de/votes/<i>id</i>[.format]</code><br>
	Method: <code>DELETE</code><br>
	Formats: <code>json, xml, html</code><br>
	Requires authentication: Yes<br><br>
	Returns a system message in the specified format, reporting whether the deletion has been successful or not.
	<br><br>
	
	<strong>data formats</strong>
	<b>vote entities</b><br>
	Votes can be read and written as either JSON, XML or HTML data.
	<br><br>
	JSON Example:
<pre>{
	"tweet_id": 1265072567, 
	"user_id": 14443226, 
	"id": 55, 
	"weight": -1.0, 
	"time": "Sun Mar  1 11:41:30 2009"
}</pre>
	XML Example:
<pre>&lt;?xml version='1.0' encoding='UTF-8'?&gt;
&lt;vote&gt;
	&lt;id&gt;55&lt;/id&gt;
	&lt;tweet_id&gt;1265072567&lt;/tweet_id&gt;
	&lt;user_id&gt;14443226&lt;/user_id&gt;
	&lt;weight&gt;-1.0&lt;/weight&gt;
	&lt;time&gt;Sun Mar  1 11:41:30 2009&lt;/time&gt;
&lt;/vote&gt;</pre>
	
	<br><br>
	
	<b>system messages</b><br>
	System messages are returned whenever no other response is available. They contain two fields:
 	<ul>
		<li><code>status</code>: a status type descriptor, i.e. <code>error</code> or <code>success</code>.</li>
		<li><code>message</code>: a plain-text description of the event.</li>
	</ul>
	System messages are encoded in the format specified by the client's request. An appropriate HTTP status 
	code is set whenever possible.<br><br>
	JSON Example:
<pre>HTTP/1.0 404 Not Found
Date: Sun, 08 Mar 2009 20:36:32 GMT
Content-Type: text/html; charset=utf-8
Pragma: no-cache
Cache-Control: no-cache
Content-Length: 47

{
	"status": "error", 
	"message": "No such vote."
}</pre>
<br>
XML Example:
<pre>HTTP/1.0 404 Not Found
Date: Sun, 08 Mar 2009 20:37:31 GMT
Content-Type: text/html; charset=utf-8
Pragma: no-cache
Cache-Control: no-cache
Content-Length: 110

<?xml version='1.0' encoding='UTF-8'?>
&lt;status&gt;
	&lt;status&gt;error&lt;/status&gt;
	&lt;message&gt;No such vote.&lt;/message&gt;
&lt;/status&gt;
</pre>
	
	
</div>