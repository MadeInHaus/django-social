import json
from datetime import datetime
import time
import requests
from twython import Twython, TwythonError
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
        try:
            twitter = self._create_twython_object()
        except:
            return
        try:
            log.warning('[twitter] search_term:{}'.format(term.search_term))
            log.warning('[twitter] max_id:{}'.format(max_id))
            response = twitter.search(q=term.search_term, count='100', max_id=max_id)
        except TwythonError:
            log.error('[twython error] hit twitter too much!')
            return
        tweets = response.get('statuses',None)
        if len(tweets) == 0:
            log.warning('[twitter] no tweets for search term {}'.format(term.search_term))
            return
        for tweet in tweets:
            try:
                dj_tweet = TwitterMessage.create_from_json(tweet, term)
            except:
                # item already exists, stop reading
                log.warning('[twitter] kicking out (tweet exists)')
                return
            epoch = int(time.mktime(dj_tweet.date.timetuple()))
            
            if epoch < term.search_until:
                # tweet was created before your limit, stop
                log.warning('[twitter] kicking out (tweet is too old)')
                return
            

        # print(response.get('search_metadata'))
        # sometimes the max_id_str was coming back empty... had to get it here instead
        try:
            max_id = parse_qs(urlparse(response.get('search_metadata').get('next_results')).query).get('max_id')
        except:
            log.warning('issues with twitter:{}'.format(response.get('search_metadata')))
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


