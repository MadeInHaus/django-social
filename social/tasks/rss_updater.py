import json
from datetime import datetime
import time
import requests
import feedparser

from .. import settings

from logging import getLogger
from social.models import RSSAccount
log = getLogger('rss.updater')


class RSSUpdater():
    def __init__(self):
        pass


    def update(self):
        for account in RSSAccount.objects.all():
            log.warning('[RSS updater account: {}]'.format(account))
            d = feedparser.parse(account.feed_url)
            if d.bozo:
                log.error('[RSS updater failed to parse: {}]'.format(account))
                continue
            for entry in d.entries:
                log.warning("{} {}".format(entry['id'], entry['published']))
                