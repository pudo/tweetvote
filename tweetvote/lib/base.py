"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import request, response, session
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