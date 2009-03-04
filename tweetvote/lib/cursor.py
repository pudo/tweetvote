from copy import copy
import simplejson as json
import twitter

from pylons import request, session, g

import tweetvote.model as model
import tweetvote.lib.classify as classify
import tweetvote.lib.twapi as twapi


class TwitterCursor(object):
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = dict()
        self.searches = []
        
    def addSearch(self, term):
        if not term in self.searches:
            self.searches.append(term)
        
    def addItems(self, items, source=None):
        for item in items:
            sources = [source]
            if item in self.items.keys() \
                and not source in self.items[item]:
                sources += self.items[item]
            self.items[item] = sources
        
    def loadNext(self, since_id=None, count=20):
        if count > 100:
            raise ValueError("Too many elements requested.")
        api = twapi.create_api()
        self.addItems(self.fetchFriendsTimeline(api, count*2, since_id=since_id), None)
        for term in self.searches:
            results = self.fetchSearch(api, term, count*2, since_id=since_id)
            self.addItems(results, term)
        results = self.matchResults(sorted(self.items.keys()), since_id, count)
        results_json = []
        for result in results:
            status = twapi.get_status(result)
            if not status:
                continue # someone deleted their status, most likely
            rdata = '"status": %s,' % status.AsJsonString()
            vote = model.findVoteByUserAndTweet(self.user_id, result)
            if vote:
                rdata += '"vote": %s,' % vote.toJSON()
            sources = filter(None, self.items[result])
            rdata += '"sources": %s,' % json.dumps(sources)
            rdata += '"score": %.2f' % classify.classify(status, self.user_id)
            results_json.append(rdata)
        return "[{%s}]" % "},{".join(results_json)
        
    def matchResults(self, results, since_id, count):
        if since_id:
            matching = [r for r in results if r > since_id]
            return matching[max(0, len(matching)-count):len(matching)]
        return results[:count]
    
    def fetchSearch(self, api, term, count, since_id=None):
        key = twapi.search_cache_key(term)
        results = candidates = g.cache.get(key)
        if candidates:
            # check if cached results are sufficient
            if since_id:
                candidates = [c for c in candidates if c > since_id]
            if len(candidates) >= count:
                return candidates
            if since_id and max(results) > since_id:
                since_id = max(results)
        else:
            results = []
        
        results = self.fetchSearchResults(api, term, count, since_id=since_id) + results
        g.cache.set(key, results, time=300)
        return results
        
    
    def fetchSearchResults(self, api, term, count, since_id=None):
        results = page = self.fetchSearchResultsSince(api, term, count, since_id=since_id)
        while since_id and len(page):
            since_id = max(page)
            page = self.fetchSearchResultsSince(api, term, count, since_id=since_id)
            results = page + results
        return results
        
    def fetchSearchResultsSince(self, api, term, count, since_id=None):
        url = 'http://search.twitter.com/search.json'
        parameters = {}
        parameters['q'] = term
        parameters['rpp'] = count
        if since_id:
            parameters['since_id'] = since_id
        obj = twapi.ip_api._FetchUrl(url, parameters=parameters)
        data = json.loads(obj)
        #api._CheckForTwitterError(data)
        return [x.get('id') for x in data['results']]

    def fetchFriendsTimeline(self, api, count, since_id=None):
        key = "utl_%d" % session['user_id']
        results = candidates = g.cache.get(key)
        if candidates:
            
            # check if cached results are sufficient
            if since_id:
                candidates = [c for c in candidates if c > since_id]
            if len(candidates) >= count:
                return candidates
            if since_id and max(results) > since_id:
                since_id = max(results)
        else:
            results = []
        
        for i in xrange(1, 1500/count): # lets be gentle ;-)
            page = self.fetchFriendsTimelinePage(api, count, since_id=since_id, page=i)
            results = page + results
            if not len(page) or not since_id:
                break
        
        g.cache.set(key, results, time=60)
        return results

    def fetchFriendsTimelinePage(self, api, count, since_id=None, page=1):
        url = 'http://twitter.com/statuses/friends_timeline.json'
        parameters = {}
        parameters['page'] = page
        parameters['count'] = count
        if since_id:
            parameters['since_id'] = since_id
        obj = api._FetchUrl(url, parameters=parameters)
        data = json.loads(obj)
        #api._CheckForTwitterError(data)
        statuses = [twitter.Status.NewFromJsonDict(x) for x in data]
        for s in statuses:
            g.cache.set(twapi.status_cache_key(s.id), s)
        return [s.id for s in statuses]
        
        
twapi.set_credentials("pudo", "worm256")
user_id = 14443226
cur = TwitterCursor(user_id)
cur.addSearch("#spectrial")