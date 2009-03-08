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
        return "%s%s" % (self.prefix, md5.new(key).hexdigest())


ip_api = twitter.Api()

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
        request.environ['twitter_api'] = api
        return api
        
    return None
    
def get_status(id):
    key = status_cache_key(id)
    status = g.cache.get(key)
    if not status:
        try:
            status = ip_api.GetStatus(id)
        except HTTPError, he:
            if he.code == 403: 
                # why use twitter and fucking protect your profile? assholes.
                status = create_api().GetStatus(id)
        g.cache.set(key, status)
    return status
    
def get_user(id):
    key = "user_%s" % id
    user = g.cache.get(key)
    if not user:
        user = ip_api.GetUser(id)
        g.cache.set(key, user, time=86400*2)
    return user
    
def uid_by_name(name):
    if name:
        try:
            return int(name)
        except ValueError, ve:
            user = get_user(name.encode("ascii"))
            if user:
                return user.id
    return None
        
def status_cache_key(id):
    return "status_%s" % id
    
def search_cache_key(term):
    return "search_%s" % md5.new(term).hexdigest()