import logging
from datetime import datetime

try:
	import cElementTree as etree
except ImportError, ie:
	import ElementTree as etree
	
import simplejson as json

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest

import formencode
from formencode import validators

import tweetvote.model as model
from tweetvote.lib.base import *
from tweetvote.lib import twapi
from tweetvote.lib import classify

log = logging.getLogger(__name__)

class VoteCreateForm(formencode.Schema):
    allow_extra_fields = True
    tweet_id = validators.Int(not_empty=True)
    weight = validators.Number(not_empty=True)

class VoteUpdateForm(formencode.Schema):
    allow_extra_fields = True
    weight = validators.Number(not_empty=True)

class VotesController(BaseController):
    """REST Controller styled on the Twitter API"""

    @rest.dispatch_on(POST='create')
    def index(self, format='html'):
        """GET /votes: All items in the collection"""
        if request.method in ['POST', 'PUT']:
            print "Patch patch patch"
            return self.create(format=format)
        print "FORMAT", format
        return formatted_status("n/a", code=404, format=format)
        
        # url('votes')
        
    def _get_vote(self, id, format, check_owner=True):
        try:
            id = int(id)
        except ValueError, ve:
            raise StatusException("Invalid vote ID", http_code=404, format=format)

        vote = model.findVoteById(id)

        if not vote:
            raise StatusException("No such vote.", http_code=404, format=format)
        if check_owner:
            user_id = session['user_id']
            if user_id != vote.user_id:
                raise StatusException("Not your vote.", http_code=401, format=format)
                
        return vote
    
    @rest.dispatch_on(GET='view', HEAD='view', POST='update', PUT='update', DELETE='delete')
    def vote_dispatch(self, id, format='html'):
        abort(405)
    
    @with_format()    
    def view(self, id, format='html', **kw):
        try:
            vote = self._get_vote(id, format, check_owner=False)
            
            if format == 'json':
                return vote.toJSON()
            elif format == 'xml':
                xml = vote.toXML()
                return etree.tostring(xml, encoding='UTF-8')

            c.vote = vote
            return render("vote.mako")
        except StatusException, se:
            return se.message
    
    @with_auth
    @with_format()
    def create(self, format='html', **kw):
        """POST /votes: Create a new item"""
        
        form = dict()
        try:
            form = rest_validate(VoteCreateForm)
        except formencode.Invalid, i:
            return fstatus(i.message, format=format, http_code=400)
        
        user_id = session['user_id']
        tweet_id = form.get("tweet_id")
        
        if model.findVoteByUserAndTweet(user_id, tweet_id):
            return fstatus("This rating already exists, please update it instead.", 
                format=format, http_code=409)
        
        model.meta.Session.begin()
        vote = model.Vote(tweet_id, user_id, 
            weight=form.get("weight"))
        model.meta.Session.add(vote)
        model.meta.Session.commit()
        
        classify.learn_vote(vote)
        log.debug("Created: %s" % vote)
        
        return self.view(vote.id, format=format, **kw)

    @with_auth
    @with_format()
    def update(self, id, format='html', **kw):
        """PUT /votes/id: Update an existing item"""
        try:
            vote = self._get_vote(id, format)
            
            form = dict()
            try:
                form = rest_validate(VoteUpdateForm)
            except formencode.Invalid, i:
                return fstatus(i.message, format=format, http_code=400)
            
            
            model.meta.Session.begin()
            vote.weight=form.get("weight")
            vote.time = datetime.utcnow()
            model.meta.Session.merge(vote)
            model.meta.Session.commit()
            classify.unlearn_vote(vote)
            classify.learn_vote(vote)
            log.debug("Updated: %s" % vote)
            
            return self.view(vote.id, format=format, **kw)
        except StatusException, se:
            return ve.message
    
    @with_auth
    @with_format()
    def delete(self, id, format='html', **kw):
        """DELETE /votes/id: Delete an existing item"""
        try:
            vote = self._get_vote(id, format)
            
            model.meta.Session.begin()
            model.meta.Session.delete(vote)
            model.meta.Session.commit()
            
            classify.unlearn_vote(vote)
            
            return fstatus("Deleted.", format=format)
        except StatusException, se:
            return ve.message
        