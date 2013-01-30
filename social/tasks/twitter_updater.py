import json
from datetime import datetime
import time
import requests
from twython import Twython

from .. import settings

class TwitterUpdater():
    def __init__(self):
        self.t = Twython(app_key=settings.SOCIAL_TWITTER_CONSUMER_KEY,
            app_secret=settings.SOCIAL_TWITTER_CONSUMER_SECRET)
        
        auth_props = self.t.get_authentication_tokens()


    def update(self):
        pass
