from tweetvote.tests import *

class TestTwitteratorController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='twitterator', action='index'))
        # Test response...
