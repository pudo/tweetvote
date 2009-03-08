"""The base Controller API

Provides the BaseController class for subclassing.
"""

try:
	import cElementTree as etree
except ImportError, ie:
	import ElementTree as etree
	
import simplejson as json
import base64

import formencode
from formencode import validators
from decorator import decorator

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from paste.httpexceptions import HTTPUnauthorized
from paste.httpheaders import *

from tweetvote.model import meta
from tweetvote.lib import twapi

class BaseController(WSGIController):

    def http_auth(self, environ, start_response):
        authorization = AUTHORIZATION(environ)
        if authorization:
            (authmeth, auth) = authorization.split(' ', 1)
            if 'basic' == authmeth.lower():
                username, password = auth.strip().decode('base64').split(':', 1)
                if twapi.set_credentials(username, password):
                    return None
            head = WWW_AUTHENTICATE.tuples('Basic realm="Tweetvote API"')
            response = HTTPUnauthorized(headers=head)
            return response.wsgi_application(environ, start_response)
        

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        
        error = self.http_auth(environ, start_response)
        if error: 
            return error
        
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

def logged_in():
    return 'user_id' in session
    
def require_login():
    if not logged_in():
        abort(401)
        
def with_auth(**kw):
    def new(meth, *args, **kws):
        require_login()
        return meth(*args, **kws)
    return decorator(new)

MIMETYPES = {
    'json': 'text/javascript',
    'atom': 'text/xml',
    'rss': 'text/xml'
}

def fstatus(message, format='html', status='success', http_code=200):
    if http_code not in [200, 302] and status == 'success':
        status = 'error'
    response.status_int = http_code
    if format == 'xml' or format == 'atom' or format == 'rss':
        xml = etree.Element('status')
        etree.SubElement(xml, 'status').text = status
        etree.SubElement(xml, 'message').text = message
        return etree.tostring(xml, encoding='UTF-8')
    elif format == 'json':
        return json.dumps({
            'status': status,
            'message': message
        })
    else:
        c.status = status
        c.message = message
        return render('status.mako')
        
class StatusException(Exception):
    
    def __init__(self, *a, **kw):
        self.message = fstatus(*a, **kw)

def get_request_fields():
    ctype = request.content_type
    if ctype.startswith('text/xml'):
        vote = etree.fromstring(request.body)
        return dict([(c.tag, c.text) for c in vote])
    elif ctype.startswith('text/javascript'):
        return json.loads(request.body)
    else:
        #  rest will be interpreted as urlencoded form
        return request.params
        
def rest_validate(schema, fields=None):
    if not fields:
        fields = get_request_fields()
    return schema().to_python(fields, None)
    

def with_format(valid=['html', 'json', 'xml']):
    def extract_format  (meth, *args, **kws):
        if 'format' in kws.keys():
            format = kws['format'].lower().strip()
            if not format in valid:
                abort(404)
            kws['format'] = format

            mime = "text/%s" % format 
            if format in MIMETYPES.keys():
                mime = MIMETYPES[format]
            response.content_type = mime
        return meth(*args, **kws)
    return decorator(extract_format)


#################################################
#
# SEARCHES IN SESSION SUPPORT
#

def session_searches():
    if not 'searches' in session.keys():
        session['searches'] = []
    return session['searches']

def add_search(term):
    searches = session_searches()
    if not term in searches:
        searches.append(term)
    print ", ".join(searches)
    session['searches'] = searches
    session.save()
    return searches
    
def del_search(term): 
    searches = session_searches()
    try:
        searches.remove(term)
    except ValueError, ve:
        pass # even better
    session['searches'] = searches
    session.save()
    return searches