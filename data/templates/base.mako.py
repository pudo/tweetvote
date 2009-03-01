from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1235875313.4780841
_template_filename='/Users/fl/Code/tweetvote/tweetvote/templates/base.mako'
_template_uri='/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n\t<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n\t<title>tweetvote: ')
        # SOURCE LINE 5
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n\t<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>\n\t<script type="text/javascript">\n\t\n\t</script>\n\t\n\t<style>\n\t\tbody, td {\n\t\t\tfont-size: 0.9em;\n\t\t\tfont-family: \'Lucida Grande\', Calibri, Helvetica, sans-serif;\n\t\t}\n\t\tbody {\n\t\t\tbackground-color: #00d8ff;\n\t\t}\n\t\t\n\t\t#logo {\n\t\t\tmargin-left: auto;\n\t\t\tmargin-right: auto;\n\t\t\tpadding: 3em;\n\t\t\twidth: 238px;\n\t\t}\n\t\t\n\t\t#page_container {\n\t\t\twidth: 444px;\n\t\t\tmargin-left: auto;\n\t\t\tmargin-right: auto;\n\t\t}\n\t\t\n\t\t#page {\n\t\t\tbackground-color: white;\n\t\t\tpadding: 0 1em 0 1em;\n\t\t\tcolor: #333333;\n\t\t}\n\t\t\n\t\t#page a {\n\t\t\tcolor: #000000;\n\t\t\ttext-decoration: none;\n\t\t\tfont-weight: bold;\n\t\t}\n\t\t\n\t\t#footer {\n\t\t\tmargin-left: auto;\n\t\t\tmargin-right: auto;\n\t\t\tpadding: 3em;\n\t\t\twidth: 20em;\n\t\t\ttext-align: center;\n\t\t\tcolor: white;\n\t\t}\n\t\t\n\t\t#footer a {\n\t\t\ttext-decoration: none;\n\t\t\tcolor: white;\n\t\t}\n\t\t\n\t\t#tweet, #no_tweet {\n\t\t\tdisplay: none;\n\t\t}\n\t\t\n\t\t#tweet {\n\t\t\twidth: 100%;\n\t\t}\n\t\t\n\t\t#tweet #header {\n\t\t\tpadding: 0.5em 0 0.7em 0;\n\t\t\tfont-family: Georgia, serif;\n\t\t\tfont-size: 1.8em;\n\t\t\tcolor: #bbbbbb;\n\t\t}\n\t\t\n\t\t#tweet td {\n\t\t\tvertical-align: top;\n\t\t}\n\t\t\n\t\t#tweet .message {\n\t\t\tfont-size: 1.2em;\n\t\t}\n\t\t\n\t\t#tweet .time {\n\t\t\tfont-size: 0.8em;\n\t\t\tcolor: #bbbbbb;\n\t\t\ttext-align: right;\n\t\t}\n\t\t\n\t\t#tweet .profile_icon {\n\t\t\tmargin: 0 0.5em 0 0;\n\t\t\tborder: 1px solid #333333;\n\t\t}\n\t\t\n\t\t#tweet .votes {\n\t\t\ttext-align: center;\n\t\t}\n\t\t\n\t\t#tweet .votes #vote_up {\n\t\t\tpadding-right: 1em;\n\t\t}\n\t\t\n\t\t#tweet .votes #vote_down {\n\t\t\tpadding-left: 1em;\n\t\t}\n\t\t\n\t\t#tweet .votes img {\n\t\t\tmargin: 1em;\n\t\t}\n\t\t\n\t\t#please_wait {\n\t\t\tdisplay: none;\n\t\t\twidth: 444px;\n\t\t\ttext-align: center;\n\t\t\tcolor: black;\n\t\t}\n\t\t\n\t\t.hint {\n\t\t\twidth: 100%;\n\t\t\tpadding: 1em;\n\t\t\tfont-size: 0.7em;\n\t\t\ttext-align: center;\n\t\t}\n\t\t\n\t\tstrong {\n\t\t\tfont-family: Georgia, serif;\n\t\t\tfont-size: 2em;\n\t\t\tfloat: right;\n\t\t\tfont-weight: normal;\n\t\t\tcolor: black;\n\t\t}\n\t\t\n\t\t.login {\n\t\t\tpadding: 1em 0 0.3em 0;\n\t\t}\n\t\t\n\t\t.login label {\n\t\t\tfloat: left;\n\t\t\twidth: 40%;\n\t\t\tmargin: 0.5em 0 0 0;\n\t\t}\n\t\t\n\t\t.login input {\n\t\t\tmargin: 0.4em 0 0 0;\n\t\t\tpadding: 0.2em;\n\t\t\tdisplay: block;\n\t\t\tfont-size: 0.8em;\n\t\t}\n\t\t\n\t\t.login input[type=submit] {\n\t\t\tborder: 1px solid white;\n\t\t\tbackground-color: #d4d700;\n\t\t\tcolor: white;\n\t\t\tfont-size: 1em;\n\t\t\tpadding: 0.3em 0.8em 0.3em 0.8em;\n\t\t\tmargin: 0.5em;\n\t\t\tfont-weight: bold;\n\t\t}\n\t\t\n\t\t.login .error-message {\n\t\t\tcolor: #ff5732;\n\t\t}\n\t\t\n\t\t.login br { display: none;}\n\t</style>\n</head>\n<body>\n\t<div id="logo"><img src="/logo.png" alt="tweetvote"></div>\n\t\n\t<div id="page_container">\n\t\t<img src="/page_top.png">\n\t\t<div id="page">\n\n\t\t')
        # SOURCE LINE 172
        __M_writer(escape(self.body()))
        __M_writer(u'\n\t\t</div>\n\t\t<img src="/page_bot.png">\n\t</div>\n\t\n\t<div id="footer">\n\t\t<a href="http://pudo.org/blog">blog</a> &middot;\n\t\t<a href="#">faq</a> &middot;\n\t\t<a href="#">api</a> &middot;\n')
        # SOURCE LINE 181
        if 'user_id' in session: 
            # SOURCE LINE 182
            __M_writer(u'\t\t\t<a href="/logout">end session</a> &middot;\n')
        # SOURCE LINE 184
        __M_writer(u'\t\t<a href="http://pudo.org/blog/about/">imprint</a>\n\t</div>\n</body>')
        return ''
    finally:
        context.caller_stack._pop_frame()


