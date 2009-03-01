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
        try:
            ftl = api.GetFriendsTimeline()
            request.environ['twitter_api'] = api
            return api
        except HTTPError, httpe:
            log.debug(httpe)
    
    return None
