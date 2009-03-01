"""The application's Globals object"""
import twitter

from pylons import config

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
        