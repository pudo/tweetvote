from urllib2 import HTTPError
import logging

import twitter

from pylons import request, session, g


log = logging.getLogger(__name__)

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
        api.SetCache(g.twitter_cache)
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
    
