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
        
        timeline = api.GetFriendsTimeline()
        for next in reversed(timeline):
            yield (next.id, next.AsJsonString())
        
        query = validators.String(if_empty=None).to_python(request.params['search'], None)
        if query:
            session['query'] = query
            session.save()
            
            for id in self._search_entries(query):
                status = twapi.get_status(id)
                yield (id, status.AsJsonString())
                
    def _search_entries(self, query):
        
        # todo bring this into twapi or submit a patch on the twitter API
        
        key = "search_%s_%s" % (session['user_id'], query.encode('ascii', 'xmlcharrefreplace'))
        url = "http://search.twitter.com/search.json?q=%s" \
                    % urllib2.quote(query)
        
        seen = []
        entries = g.cache.get(key)
        while True: 
            if not entries or len(entries) == 0:
                log.debug("Reloading search feed for: %s from %s" % (query, url))
                search = urllib2.urlopen(url)
                entries = json.loads(search.read()).get('results')
                search.close()
                if not entries or len(entries) == 0: 
                    return
                fresh = [e.get('id') in seen for e in entries]
                if not False in fresh:
                    return
                        
            while entries:
                entry = entries.pop()
                if not entries:
                    g.cache.delete(key)
                else:
                    g.cache.set(key, entries, time=300)
                id = entry.get('id')
                seen.append(id)
                yield id
                
                
    def _score_json(self, s):
        # the JSON shuffle: cut it up, patch it, sow it shut
        obj = json.loads(s)
        status = twapi.get_status(obj.get('id'))
        obj['score'] = "%.1f" % classify.classify(status, session['user_id'])
        return json.dumps(obj)

    
    def next(self):
        require_login()
        response.headers['Content-type'] = 'text/javascript'
        
        for (id, obj) in self._find():
            if not model.findVoteByUserAndTweet(session['user_id'], id):
                return self._score_json(obj)
        
        return 'false'
        
