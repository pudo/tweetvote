import logging

try:
	import cElementTree as etree
except ImportError, ie:
	import ElementTree as etree
	
import simplejson as json

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

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
    """REST Controller styled on the Atom Publishing Protocol"""

    def __before__(self):
        require_login()
        
    def _status(self, message, format='html', status='success', code=200):
        if code not in [200, 302, 410]:
            status = 'error'
        response.status_code = code
        if format == 'xml':
            status = etree.Element('status')
            etree.SubElement(status, 'status').text = status
            etree.SubElement(status, 'message').text = message
            return etree.tostring(status, encoding='UTF-8')
        elif format == 'json':
            return json.dumps({
                'status': status,
                'message': message
            })
        else:
            c.status = status
            c.message = message
            return render('status.mako')

    def index(self, format='html'):
        """GET /votes: All items in the collection"""
        
        
        # url('votes')

    @validate(schema=VoteCreateForm(), form="new")
    def create(self):
        """POST /votes: Create a new item"""
        user_id = session['user_id']
        tweet_id = self.form_result.get("tweet_id")
        
        log.debug("Create: %d, %d" % (user_id, tweet_id))
        
        if model.findVoteByUserAndTweet(user_id, tweet_id):
            response.status_code = 409
            form = render("vote_new.mako")
            return formencode.htmlfill.render(form, 
                defaults=self.form_result,
                errors={'tweet_id': "This rating already exists. Use PUT to update."})
        
        model.meta.Session.begin()
        vote = model.Vote(tweet_id, user_id, 
            weight=self.form_result.get("weight"))
        model.meta.Session.merge(vote)
        model.meta.Session.commit()
        
        classify.learn_vote(vote)
        log.debug("Created: %s" % vote)
        
        print "JSON", vote.json()
        print "XML", etree.tostring(vote.xml())
        
        c.vote = vote
        return render("vote_edit.mako")


    def new(self, format='html'):
        """GET /votes/new: Form to create a new item"""
        # this would really require a tweet_id, so we'll forward
        redirect_to('/classify')        

    @validate(schema=VoteUpdateForm(), form="new")
    def update(self, id):
        """PUT /votes/id: Update an existing item"""
                
        log.debug("Update: %d" % id)
        
        user_id = session['user_id']
        try:
            vote = model.findVoteById(int(id))
            if not vote:
                abort(404, "No such vote.")
            if user_id != vote.user_id:
                abort(401, "Not your vote.")
            model.meta.Session.begin()
            vote.weight=self.form_result.get("weight")
            model.meta.Session.merge(vote)
            model.meta.Session.commit()
            classify.unlearn_vote(vote)
            classify.learn_vote(vote)
            log.debug("Updated: %s" % vote)
            
            c.vote = vote
            return render("vote_edit.mako")
            
        except ValueError, ve:
            abort(404, "Invalid vote ID!")
        
    def delete(self, id):
        """DELETE /votes/id: Delete an existing item"""
        user_id = session['user_id']
        tweet_id = self.form_result.get("tweet_id")

    def show(self, id, format='html'):
        """GET /votes/id: Show a specific item"""
        # url('vote', id=ID)

    def edit(self, id, format='html'):
        """GET /votes/id/edit: Form to edit an existing item"""
        
        user_id = session['user_id']
        try:
            vote = model.findVoteById(int(id))
            if not vote:
                abort(404, "No such vote.")
            if user_id != vote.user_id:
                abort(401, "Not your vote.")
            c.vote = vote
            return render("vote_edit.mako")
            
        except ValueError, ve:
            abort(404, "Invalid vote ID!")