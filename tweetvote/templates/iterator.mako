<%inherit file="base.mako" />
<%def name="title()">Tweet Classification</%def>

<table border="0" id="tweet">
	<tr>
		<td colspan="2" id="header">
			Give a shit?
		</td>
	</tr>
	<tr>
		<td rowspan="2">
			<img class="profile_icon" src="" alt="profile icon" />
		</td>
		<td>
			<a class="sender" href="">sender</a>: 
			<div class="message">message</div>
		</td>
	</tr>
	<tr>
		<td class="time">
			time
		</td>
	</tr>
	<tr>
		<td colspan="2" class="votes">
			<a id="vote_up" href=""><img src="/up.png" alt="up"></a>
			<a id="vote_down" href=""><img src="/down.png" alt="down"></a> 
		</td>
	</tr>
</table>
<div id="no_tweet">
	No unclassified tweets in your timeline. New tweets will be loaded automatically.
</div>
<div id="please_wait">
<img src="/gnomes.png"><br>	
Please wait, the gnomes are working...
</div>

<div class="hint">
Hint: you can also use the '+' and '-' keys to quickly classify tweets.
</div>

<script type="text/javascript">
	
	/* 
	I, the javascript victim, hereby solemnly swear to faithfully use the powers
	vested in me by the global variable, to love and despise it and to never write
	it from where it shall not be written; to never read it where it shall not be
	read. 
	*/
	pendingVote = false;
	vote = function(tweet_id, weight) {
		$("#no_tweet").hide();
		$("#tweet").hide();
		$("#please_wait").show();
		
		if (pendingVote) return;
		pendingVote = true;
	
		$.post('/votes', {'tweet_id': tweet_id, 
			              'weight': weight}, function(data, status) {
			pendingVote = false;
			if (status == 'success') {
				loadNext();
			} else {
				alert("Error while sending the vote.")
			}
		});
	}
	
	voteUp = function() {}
	voteDown = function() {}
	$("#vote_up").click(function()   { voteUp(); return false; });
	$("#vote_down").click(function() { voteDown(); return false; });
	
	$(document).keypress(function(e) {
		switch(e.which) {
			case 43: 
				voteUp(); break; // '+'
			case 45: 
				voteDown(); break; // '-'
		}
	});
	
	loadNext = function() {
		if (pendingVote) return;
		$.getJSON('/twitterator/next', function(json) {
			if (json) {
				$("#please_wait").hide();
				$("#no_tweet").hide();
				$("#tweet").show();
				$("#tweet .profile_icon").attr('src', json.user.profile_image_url);
				$("#tweet .sender").attr('href', json.user.url);
				$("#tweet .sender").text(json.user.screen_name);
				$("#tweet .message").text(json.text);
				$("#tweet .time").text(json.created_at);
				
				voteUp = function() {
					vote(json.id, 1.0);
				} 
				voteDown = function() {
					vote(json.id, -1.0);
				}
			} else {
				$("#tweet").hide();
				$("#please_wait").hide();
				$("#no_tweet").show();
				setTimeout(loadNext, 30000);
			}
			pendingVote = false;
		});
	}
	
	loadNext();
</script>