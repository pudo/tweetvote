import logging
from datetime import datetime

try:
	import cElementTree as etree
except ImportError, ie:
	import ElementTree as etree
	
import simplejson as json

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import Table, Column, Integer, String, Float, DateTime

from meta import Base
import meta

log = logging.getLogger(__name__)

class Vote(Base):
    __tablename__ = 'vote'
    
    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    tags = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=False)

    def __init__(self, tweet_id, user_id, weight=1.0, tags=None):
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.weight = weight
        self.tags = tags
        self.time = datetime.utcnow()
        
    def __repr__(self):
        return "Vote(%d,%d,%.2f)" % (self.tweet_id, self.user_id, self.weight)
        
    def tagiter(self):
        if self.tags:
            for tag in self.tags.split(','):
                yield tag.strip()
        
    def xml(self):
        vote = etree.Element("vote")
        etree.SubElement(vote, "id").text = str(self.id)
        etree.SubElement(vote, "tweet_id").text = str(self.tweet_id)
        etree.SubElement(vote, "user_id").text = str(self.user_id)
        etree.SubElement(vote, "weight").text = str(self.weight)
        etree.SubElement(vote, "time").text = str(self.time.ctime())
        return vote
        
    def json(self):
        vote = {
            'id': self.id,
            'tweet_id': self.tweet_id,
            'user_id': self.user_id,
            'weight': self.weight,
            'time': self.time.ctime()
        }
        return json.dumps(vote)
        

def findVoteById(id):
    """
    Find a vote with a given vote ID.   
    Upon failure, return None.
    """
    
    try:
        return Session.query(Vote).filter(Vote.id == id).one()
    except NoResultFound, nrf:
        log.debug('Vote ID %s not found' % id)
    except MultipleResultsFound, mrf:
        log.debug('Vote ID %s exists multiple times' % id)
        

def findUserVotes(user_id, limit=None):
    q = meta.Session.query(Vote).filter(Vote.user_id == user_id).order_by('time desc')
    if limit:
        q.limit(limit)
    return q.all()
    
def findTweetVotes(tweet_id):
    return meta.Session.query(Vote).filter(Vote.tweet_id == tweet_id).all()

def findVoteByUserAndTweet(user_id, tweet_id):
    try:
        return meta.Session.query(Vote).filter(
            and_(Vote.tweet_id == tweet_id, Vote.user_id == user_id)).one()
    except NoResultFound, nrf:
        log.debug('Vote not found')
    except MultipleResultsFound, mrf:
        log.debug('Vote exists multiple times')
    
