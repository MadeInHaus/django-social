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
        for account in TwitterAccount.objects.all():
            log.error("account: {}".format(account.__dict__))
            twitter = Twython(app_key=SOCIAL_TWITTER_CONSUMER_KEY, app_secret=SOCIAL_TWITTER_CONSUMER_SECRET, oauth_token=account.oauth_token, oauth_token_secret=account.oauth_secret)
            timeline = twitter.getUserTimeline()
            log.error("user timeline: {}".format(timeline))