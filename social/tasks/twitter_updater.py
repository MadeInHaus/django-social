import json
from datetime import datetime
import time
import requests
from twython import Twython
from urlparse import urlparse, parse_qs

from .. import settings
from ..models import TwitterAccount, TwitterSearch, TwitterMessage
from ..settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET

from logging import getLogger
log = getLogger('twitter.updater')

class TwitterUpdater():
    def __init__(self):
        pass

    def update(self):
        now = int(time.time())
        for term in TwitterSearch.objects.all():
            self._step(term)
        

    def _step(self, term, max_id=0):
        twitter = self._create_twython_object()
        response = twitter.search(q=term.search_term, count='100', max_id=max_id)
        tweets = response.get('statuses',None)
        if len(tweets) == 0:
            raise Exception("no tweets")
        for tweet in tweets:
            dj_tweet = TwitterMessage.create_from_json(tweet)
            return
            # TODO place logic here to stop stepping

        # print(response.get('search_metadata'))
        # sometimes the max_id_str was coming back empty... had to get it here instead
        max_id = parse_qs(urlparse(response.get('search_metadata').get('next_results')).query).get('max_id')
        self._step(term,max_id=max_id)
            
    def _create_twython_object(self):
        account = TwitterAccount.get_next_up()
        if not account:
            raise Exception("no twitter accounts setup")
        twitter = Twython(  app_key=SOCIAL_TWITTER_CONSUMER_KEY, 
                            app_secret=SOCIAL_TWITTER_CONSUMER_SECRET, 
                            oauth_token=account.oauth_token, 
                            oauth_token_secret=account.oauth_secret)
        return twitter


