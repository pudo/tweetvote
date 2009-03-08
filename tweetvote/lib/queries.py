import tweetvote.model as model
import twapi
from sqlalchemy import and_

def find_votes(vote_user=None, tweet_user=None, status=None, count=100, page=1):
    query = model.meta.Session.query(model.Vote)
    
    vote_user = twapi.uid_by_name(vote_user)
    if vote_user:
        query = query.filter(model.Vote.user_id == vote_user)
    
    if tweet_user:
        pass
        #query = query.filter(model.Vote.user_id == from_user)
        
    if status:
        query = query.filter(model.Vote.tweet_id == status)
    
    query = query.order_by(model.Vote.time.desc())
    query = query.limit(count)
    query = query.offset((page - 1) * count)
    
    return query.all()
    