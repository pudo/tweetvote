import logging

import simplejson as json

import formencode
from formencode import validators

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetvote.lib.base import *

log = logging.getLogger(__name__)

class SearchController(BaseController):

    @with_auth()
    def index(self, **kw):
        searches = session_searches()
        return json.dumps(session_searches())
    
    @with_auth()
    def add(self, **kw):
        response.content_type = 'text/javascript'
        try:
            term = validators.String(empty=False).to_python(request.params['term'], None)
            add_search(term)
            return json.dumps({'term': term})
        except Exception, e:
            return fstatus(repr(e), http_code=400, format='json')
    
    @with_auth()
    def delete(self, **kw):
        response.content_type = 'text/javascript'
        try:
            term = validators.String(empty=False).to_python(request.params['term'], None)
            del_search(term)
            return json.dumps({'term': term})
        except Exception, e:
            return fstatus(repr(e), http_code=400, format='json')
