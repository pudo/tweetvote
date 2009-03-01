"""The application's Globals object"""
import twitter
import memcache 

from pylons import config

import classify

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        here = config['here']
        
        self.twitter_cache = twitter._FileCache(root_directory="%s/data/twitter" % here)
        
        if not 'memcached.server' in config:
            config['memcached.server'] = "127.0.0.1:11211"
        self.cache = memcache.Client([config['memcached.server']])
        
        
        classify.retrain()
        