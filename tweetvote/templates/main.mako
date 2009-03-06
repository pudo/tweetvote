<%inherit file="base.mako" />
<%def name="title()">What's good?</%def>

<div class="searches">
<div class="user_tag"><span>${session.get('username')}</span></div>
<form id="search_add_form">
<input id="search_add" />
</form>
<div id="protosearch" class="search_tag" style="display: none;"><span>#spectrial</span></div>
</div>

<div id="timeline">
<div id="prototype" class="tweet" style="display: none;">
		<div class="leftbox">&nbsp;</div>
		<div class="box">
			<img width="48" height="48" class="profile_icon" src="" alt="profile icon" />
			<div class="content">
				<a target="_new" href="#" class="sender">(nobody)</a>
				<span class="text">(no text)</span>
				<div class="meta">
					<span class="created_at">time</span>, <b><span class="score">score</span>pts</b>
				</div>
			</div>
		</div>
		<div class="rightbox">&nbsp;</div>
</div>
</div>
