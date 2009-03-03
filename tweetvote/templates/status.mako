<%inherit file="base.mako" />
<%def name="title()">{c.status}</%def>

<strong>{c.status}</strong>
<div style="clear: both;"></div>
{c.message}