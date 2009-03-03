from urllib2 import HTTPError
import logging
from time import time
import md5

import twitter

from pylons import request, session, g


log = logging.getLogger(__name__)

class MemcacheCache(object):
    
    def __init__(self, client, prefix='twitter_'):
        self.client = client
        self.prefix = prefix
        
    def Get(self, key):
        return self.client.get(self._GetKey(key))
    
    def Set(self, key, val):
        key = self._GetKey(key)
        self.client.set(key, val)
        self.client.set("%s_mod" % key, time())
        
    def Remove(self, key):
        key = self._GetKey(key)
        self.client.delete(key, val)
        self.client.delete("%s_mod" % key, time())
        
    def GetCachedTime(self, key):
        return self.client.get("%s_mod" % self._GetKey(key))
        
    def _GetKey(self, key):
        return "%s%s" % (md5.new(key).hexdigest(), self.prefix)




def set_credentials(username, password):
    session['username'] = username
    session['password'] = password
    
    api =  create_api()
    if api:
        session['user_id'] = api.GetUser(api._username).id
    else:
        session.clear()
    session.save()
    return api
    
def create_api():
    if 'twitter_api' in request.environ:
        return request.environ['twitter_api']
    
    if 'username' in session and 'password' in session:
        api = twitter.Api(username=session['username'], 
                          password=session['password'])        
        api.SetCache(MemcacheCache(g.cache))
        api.SetCacheTimeout(15)
        try:
            ftl = api.GetFriendsTimeline()
            request.environ['twitter_api'] = api
            return api
        except HTTPError, httpe:
            #print "CODE: ", dir(httpe)
            log.debug(httpe)
    
    return None
    
def get_status(id):
    key = "status_%s" % id
    status = g.cache.get(key)
    if not status:
        status = create_api().GetStatus(id)
        g.cache.set(key, status)
    return status
    
def get_user(id):
    key = "user_%s" % id
    user = g.cache.get(key)
    if not user:
        user = create_api().GetUser(id)
        g.cache.set(key, user, time=86400*2)
    return user
    
