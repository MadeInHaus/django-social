import json
from datetime import datetime
import time
import requests
from twython import Twython

from .. import settings
from ..models import TwitterAccount
from ..settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET

from logging import getLogger
log = getLogger('twitter.updater')

class TwitterUpdater():
    def __init__(self):
        pass

    def update(self):
        account = TwitterAccount.get_next_up()
        if not account:
            return 
        print(account)
        print(account.poll_count)
        twitter = Twython(  app_key=SOCIAL_TWITTER_CONSUMER_KEY, 
                            app_secret=SOCIAL_TWITTER_CONSUMER_SECRET, 
                            oauth_token=account.oauth_token, 
                            oauth_token_secret=account.oauth_secret)
        tweets = twitter.search(q='python')
        #log.error("user timeline: {}".format(tweets))
