from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1235875389.8339069
_template_filename='/Users/fl/Code/tweetvote/tweetvote/templates/login.mako'
_template_uri='/login.mako'
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
        __M_writer(u'\n<a href="http://twitter.com">twitter</a> asked millions one question: <br>\n<strong>what are you doing?</strong>\n<div style="clear: both;"></div>\n<br>\n<br>\n<b>tweetvote</b> asks a new question: <br>\n<strong>do you give a shit?</strong>\n<div style="clear: both;"></div>\n<br>\n<br><br>\nOn tweetvote, you rate tweets. Over time, this will allow us to <b>create message \nfilters</b> that can adapt to your interests, give you the <b>tweets you want to see</b>, \nwhile <b>hiding the chitchat</b> you really don\'t care about. \n<br><br>\n<strong>help now</strong>\n<div style="clear: both;"></div>\n<form class="login" name="login" method="post" action="/login">\n\t<label for="username">Twitter Username:</label>\n\t<input name="username" type="text" />\n\n\t<label for="password">Password:</label>\n\t<input type="password" name="password">\n\t\n\t<label for="submit">&nbsp;</label>\n\t<input name="submit" type="submit" class="submit" value="Login"/>\n</form>\n<div style="clear: both;"></div>\n\n<div class="hint">\nYour password will never be saved on our \nservers and is only used to identify you and to communicate with Twitter.\n\nOnce Twitter has finished OAuth support, we\'ll offer a more secure \nmethod to log into tweetvote. \n</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'Welcome')
        return ''
    finally:
        context.caller_stack._pop_frame()


