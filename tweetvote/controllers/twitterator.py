import logging
from datetime import datetime, timedelta
import urllib2

import feedparser
import simplejson as json

import formencode
from formencode import validators

from pylons import request, response, session, tmpl_context as c, g
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

from tweetvote.lib.base import *
import tweetvote.lib.twapi as twapi
import tweetvote.lib.cursor as cursor
import tweetvote.lib.classify as classify
import tweetvote.model as model

log = logging.getLogger(__name__)

class TwitteratorController(BaseController):

    @with_auth
    def index(self, **kw):
        return render('/main.mako')
    
    @with_auth
    def next(self, **kw):
        since_id = None
        try:
            if 'since_id' in request.params:
                since_id = int(request.params['since_id'])
        except ValueError, ve:
            pass
        user_id = session['user_id']
        cur = cursor.TwitterCursor(user_id)
        for search in session_searches():
            cur.addSearch(search)
        res = cur.loadNext(since_id=since_id, count=20)
        #print res
        return res