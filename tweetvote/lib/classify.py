import os, os.path
import re
import unicodedata
import urllib2

from reverend.thomas import Bayes
from BeautifulSoup import BeautifulSoup

from pylons import config

import twapi, tokenizer
import tweetvote.model as model

UP = 'up'
DOWN = 'down'
GLOBAL = 'global'

class StatusTokenizer(object):
    HASHTAG = re.compile("#([\w\-_\.+:=]+\w)")
    user_pattern = "@([\w\-_]+)"
    USER = re.compile(user_pattern)
    REPLY = re.compile("^ ?" + user_pattern)
    RT = re.compile("((rt)|(retweet)|(quoth)) ?%s" % user_pattern, re.I) # disable case
    URL = re.compile("(http:\/\/[^ ]*)") # ????
    
    def __init__(self, followlinks=True, seqlength=3):
        self.api = twapi.create_api()
        self.texttok = tokenizer.UnicodeTokenizer()
        self.followlinks = followlinks
        self.seqlength = seqlength
    
    def canonical(self, text):
        if not type(text) == type(u" "): 
            text = unicode(text, 'iso-8859-1')
        return unicodedata.normalize("NFKC", text).strip().lower()
        
    def handle_url(self, url):
        yield "(url %s)" % url
        if not self.followlinks:
            return
        try: 
            pg = urllib2.urlopen(url)
            if pg.url != url:
                yield "(url-forward %s)" % url
                yield "(url %s)" % pg.url
                
            if pg.headers['content-type'].lower().startswith("text/"):
                try:
                    soup = BeautifulSoup(pg.read())
                    te = soup.findAll("title").pop().contents
                    for token in self.handle_text(te.pop()):
                        yield token
                except Exception, e:
                    pass
            else:
                yield "(content-type %s)" % pg.headers['content-type']

            pg.close()
        except Exception, e:
            yield "(invalid-url)"
            
    def handle_text(self, text):
        tokens = [self.canonical(unicode(t)) for t in self.texttok.tokenize(text)]
        for i in range(len(tokens)):
            for add in range(0, self.seqlength + 1):
                if i + add <= len(tokens):
                    yield " ".join(tokens[i:i+add])
        
    def tokenize(self, status):
        if not hasattr(status, 'id'):
            for token in self.handle_text(unicode(status)):
                yield token
            return
        
        yield u"(id %s)" % status.id
        yield u"(author %s)" % self.canonical(status.user.screen_name)
        
        for match in self.HASHTAG.finditer(status.text):
            yield u"(tag %s)" % self.canonical(match.group())
        
        for match in self.USER.finditer(status.text):
            yield u"(mentions %s)" % self.canonical(match.group())
        
        for match in self.RT.finditer(status.text):
            yield u"(rt %s)" % self.canonical(match.group(5))
            yield u"(retweet)"
        
        for match in self.REPLY.finditer(status.text):
            yield u"(reply-to %s)" % self.canonical(match.group())
        
        for match in self.URL.finditer(status.text):
            for token in self.handle_url(match.group()):
                yield token
        
        for token in self.handle_text(unicode(status.text)):
            yield token


def test_tokenize():
    tok = StatusTokenizer()
    api = twapi.set_credentials("pudo", "")
    for status in api.GetFriendsTimeline():
        print "STATUS", repr(status)
        print "TOKENS", " | ".join([t.encode("ascii", "replace") for t in tok.tokenize(status)])

statustok = StatusTokenizer(followlinks=False)
guessers = {}
def get_bayes(id=GLOBAL):
    if not id in guessers.keys():
        bayes = Bayes(tokenizer=statustok)
        if os.path.exists(filename(id=id)):
            bayes.load(filename(id=id))
        guessers[id] = bayes
    return guessers[id]

def filename(id=GLOBAL):
    return "%s/data/bayes/%s.bay" % (config['here'], id)

def retrain():
    votes = model.meta.Session.query(model.Vote).all()
    if os.path.exists(filename()):
        os.remove(filename())
    users = []
    for vote in votes:
        #print "VOTE", repr(vote)
        if not vote.user_id in users:
            if os.path.exists(filename(id=vote.user_id)):
                os.remove(filename(id=vote.user_id))
            users.append(vote.user_id)
        learn_vote(vote, save=False)
    get_bayes().save(filename())
    for user_id in users:
        get_bayes(id=user_id).save(filename(id=user_id))


def learn_vote(vote, save=True):
    if vote.weight == 0: # float? 
        return
    clazz = UP
    if vote.weight < 0:
        clazz = DOWN
    try: # TODO remove!!!
        status = twapi.get_status(vote.tweet_id)
        learn(clazz, status, vote.user_id, save=save)
    except:
        pass


def learn(clazz, status, user_id=None, save=True):
    get_bayes().train(clazz, status)
    if user_id:
        get_bayes(id=user_id).train(clazz, status)
    
    if not save:
        return 
    # TODO: spin this off into its own thread:
    get_bayes().save(filename())
    if user_id:
        get_bayes(id=user_id).save(filename(id=user_id))

        
def classify(status, user_id):
    def classes(results):
        up = 0
        down = 0
        for (clazz, score) in results:
            if clazz == UP:
                up = score
            elif clazz == DOWN:
                down = score
        return (up, down)
        
    def proportion(up, down):
        if down == 0:
            return 0
        else: 
            return up/down
            
    globalprop = proportion(*classes(get_bayes().guess(status)))
    userprop = proportion(*classes(get_bayes(id=user_id).guess(status)))
    
    prop = (globalprop+userprop)/2.0
    return prop*100
    