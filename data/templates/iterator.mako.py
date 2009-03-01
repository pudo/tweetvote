from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1235900914.2228069
_template_filename='/Users/fl/Code/tweetvote/tweetvote/templates/iterator.mako'
_template_uri='/iterator.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, 'base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n<table border="0" id="tweet">\n\t<tr>\n\t\t<td colspan="2" id="header">\n\t\t\tGive a shit?\n\t\t</td>\n\t</tr>\n\t<tr>\n\t\t<td rowspan="2">\n\t\t\t<img class="profile_icon" src="" alt="profile icon" />\n\t\t</td>\n\t\t<td>\n\t\t\t<a class="sender" href="">sender</a>: \n\t\t\t<div class="message">message</div>\n\t\t</td>\n\t</tr>\n\t<tr>\n\t\t<td class="time">\n\t\t\ttime\n\t\t</td>\n\t</tr>\n\t<tr>\n\t\t<td colspan="2" class="votes">\n\t\t\t<a id="vote_up" href=""><img src="/up.png" alt="up"></a>\n\t\t\t<a id="vote_down" href=""><img src="/down.png" alt="down"></a> \n\t\t</td>\n\t</tr>\n</table>\n<div id="no_tweet">\n\tNo unclassified tweets in your timeline. New tweets will be loaded automatically.\n</div>\n<div id="please_wait">\n<img src="/gnomes.png"><br>\t\nPlease wait, the gnomes are working...\n</div>\n\n<div class="hint">\nHint: you can also use the \'+\' and \'-\' keys to quickly classify tweets.\n</div>\n\n<script type="text/javascript">\n\t\n\t/* \n\tI, the javascript victim, hereby solemnly swear to faithfully use the powers\n\tvested in me by the global variable, to love and despise it and to never write\n\tit from where it shall not be written; to never read it where it shall not be\n\tread. \n\t*/\n\tpendingVote = false;\n\tvote = function(tweet_id, weight) {\n\t\t$("#no_tweet").hide();\n\t\t$("#tweet").hide();\n\t\t$("#please_wait").show();\n\t\t\n\t\tif (pendingVote) return;\n\t\tpendingVote = true;\n\t\n\t\t$.post(\'/votes\', {\'tweet_id\': tweet_id, \n\t\t\t              \'weight\': weight}, function(data, status) {\n\t\t\tpendingVote = false;\n\t\t\tif (status == \'success\') {\n\t\t\t\tloadNext();\n\t\t\t} else {\n\t\t\t\talert("Error while sending the vote.")\n\t\t\t}\n\t\t});\n\t}\n\t\n\tvoteUp = function() {}\n\tvoteDown = function() {}\n\t$("#vote_up").click(function()   { voteUp(); return false; });\n\t$("#vote_down").click(function() { voteDown(); return false; });\n\t\n\t$(document).keypress(function(e) {\n\t\tswitch(e.which) {\n\t\t\tcase 43: \n\t\t\t\tvoteUp(); break; // \'+\'\n\t\t\tcase 45: \n\t\t\t\tvoteDown(); break; // \'-\'\n\t\t}\n\t});\n\t\n\tloadNext = function() {\n\t\tif (pendingVote) return;\n\t\t$.getJSON(\'/twitterator/next\', function(json) {\n\t\t\tif (json) {\n\t\t\t\t$("#please_wait").hide();\n\t\t\t\t$("#no_tweet").hide();\n\t\t\t\t$("#tweet").show();\n\t\t\t\t$("#tweet .profile_icon").attr(\'src\', json.user.profile_image_url);\n\t\t\t\t$("#tweet .sender").attr(\'href\', json.user.url);\n\t\t\t\t$("#tweet .sender").text(json.user.screen_name);\n\t\t\t\t$("#tweet .message").text(json.text);\n\t\t\t\t$("#tweet .time").text(json.created_at);\n\t\t\t\t\n\t\t\t\tvoteUp = function() {\n\t\t\t\t\tvote(json.id, 1.0);\n\t\t\t\t} \n\t\t\t\tvoteDown = function() {\n\t\t\t\t\tvote(json.id, -1.0);\n\t\t\t\t}\n\t\t\t} else {\n\t\t\t\t$("#tweet").hide();\n\t\t\t\t$("#please_wait").hide();\n\t\t\t\t$("#no_tweet").show();\n\t\t\t\tsetTimeout(loadNext, 30000);\n\t\t\t}\n\t\t\tpendingVote = false;\n\t\t});\n\t}\n\t\n\tloadNext();\n</script>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'Tweet Classification')
        return ''
    finally:
        context.caller_stack._pop_frame()


