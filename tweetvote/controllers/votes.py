import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

import formencode
from formencode import validators

import tweetvote.model as model
from tweetvote.lib.base import *
from tweetvote.lib import twapi

log = logging.getLogger(__name__)

class VoteForm(formencode.Schema):
    allow_extra_fields = True
    tweet_id = validators.Int(not_empty=True)
    weight = validators.Number(not_empty=True)


class VotesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def __before__(self):
        require_login()

    def index(self, format='html'):
        """GET /votes: All items in the collection"""
        
        
        # url('votes')

    @validate(schema=VoteForm(), form="new")
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
        
        log.debug("Created: %s" % vote)
        
        c.vote = vote
        return render("vote_edit.mako")


    def new(self, format='html'):
        """GET /votes/new: Form to create a new item"""
        # url('new_vote')

    def update(self, id):
        """PUT /votes/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('vote', id=ID),
        #           method='put')
        # url('vote', id=ID)

    def delete(self, id):
        """DELETE /votes/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('vote', id=ID),
        #           method='delete')
        # url('vote', id=ID)

    def show(self, id, format='html'):
        """GET /votes/id: Show a specific item"""
        # url('vote', id=ID)

    def edit(self, id, format='html'):
        """GET /votes/id/edit: Form to edit an existing item"""
        # url('edit_vote', id=ID)
