import logging
from datetime import datetime, timedelta

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetvote.lib.base import *
import tweetvote.lib.twapi as twapi
import tweetvote.model as model

log = logging.getLogger(__name__)

class TwitteratorController(BaseController):

    def index(self):
        require_login()
        return render('/iterator.mako')
        
    def next(self):
        require_login()
        response.headers['Content-type'] = 'text/javascript'
        
        try:
            api = twapi.create_api()
            timeline = api.GetFriendsTimeline()
            timeline.reverse()
            for next in timeline:
                if not model.findVoteByUserAndTweet(session['user_id'], next.id):
                    return next.AsJsonString()
        except Exception, e:
            log.debug(e)
        
        return 'false'
        
