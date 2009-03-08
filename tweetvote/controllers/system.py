import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

import formencode
from formencode import validators

from tweetvote.lib.base import *
from tweetvote.lib import twapi

log = logging.getLogger(__name__)

class LoginForm(formencode.Schema):
    allow_extra_fields = True
    username = validators.String(not_empty=True)
    password = validators.String(not_empty=True)

class SystemController(BaseController):

    def index(self):
        if not 'username' in session:
            redirect_to('/login')
        redirect_to('/classify')
        
    @validate(schema=LoginForm(), form="login", post_only=True)
    def login(self):
        form = render("/login.mako")
        if request.method == "POST":
            if twapi.set_credentials(self.form_result.get('username'), 
                               self.form_result.get('password')):
                redirect_to('/')
            form = formencode.htmlfill.render(form, 
                defaults = self.form_result,
                errors = {'username': "Invalid username or password."})
        return form
        
    def logout(self):
        session.clear()
        session.save()
        redirect_to('/')
        
        
    def faq(self):
        return render("/faq.mako")
        
    def api(self):
        return render("/api.mako")
