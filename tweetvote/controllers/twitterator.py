import logging
from datetime import datetime, timedelta
import urllib2

import feedparser
import simplejson

import formencode
from formencode import validators

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

from tweetvote.lib.base import *
import tweetvote.lib.twapi as twapi
import tweetvote.lib.classify as classify
import tweetvote.model as model

log = logging.getLogger(__name__)

class TwitteratorController(BaseController):

    def index(self):
        require_login()
        return render('/iterator.mako')
        
    def _find(self):
        api = twapi.create_api()
        if not api:
            return
        
        timeline = api.GetFriendsTimeline(since=datetime.utcnow()-timedelta(seconds=86400*7))
        for next in reversed(timeline):
            yield (next.id, next.AsJsonString())
        
        query = validators.String(if_empty=None).to_python(request.params['search'], None)
        if query:
            session['query'] = query
            session.save()
            url = "http://search.twitter.com/search.atom?q=%s" \
                        % urllib2.quote(query)
            log.debug("Twitter search: %s" % url)
            search = feedparser.parse(url)
            #for e in search.entries: 
            #    print "Entry: ", repr(e)
            for entry in reversed(search.entries):
                #print "E: ", entry, " id: ", entry.id
                id = int(entry.id.split(":")[2])
                url = "http://twitter.com/statuses/show/%d.json" % id
                json = urllib2.urlopen(url).read()
                yield (id, json)
                
    def _score_json(self, json):
        obj = simplejson.loads(json)
        status = twapi.get_status(obj.get('id'))
        obj['score'] = "%.1f" % classify.classify(status, session['user_id'])
        return simplejson.dumps(obj)

    
    def next(self):
        require_login()
        response.headers['Content-type'] = 'text/javascript'
        
        try:
            for (id, json) in self._find():
                if not model.findVoteByUserAndTweet(session['user_id'], id):
                    return self._score_json(json)
        except Exception, e:
            log.debug(e)
        
        return 'false'
        
