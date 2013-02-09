import json
from django.utils.datetime_safe import datetime
from time import mktime
import sys
import time
import requests
import feedparser

from django.utils.timezone import utc
from .. import settings

from ..models import RSSMessage, RSSAccount


from logging import getLogger
log = getLogger('rss.updater')


class RSSUpdater():
    def __init__(self):
        pass


    def update(self):
        for account in RSSAccount.objects.all():
            log.warning(u'[RSS updater account: {}]'.format(account))
            
            try:
                d = feedparser.parse(account.feed_url)
            except:
                log.error('[RSS updater failed to parse: {}]'.format(account))
                log.error('[RSS updater error: {} {} {}'.format(sys.exc_info()))
                continue
 
            for entry in d.entries:
                old_entry = RSSMessage.objects.filter(message_id=entry.id)
                if old_entry:
                    continue
                new_entry = RSSMessage()
                new_entry.message_type = 'post'
                new_entry.message = self.message(entry)
                new_entry.date = self.date(entry)
                new_entry.message_id = entry.id
                new_entry.deeplink = self.link(entry) 
                new_entry.blob = self.blob(entry)
                new_entry.avatar = self.avatar(entry)
                new_entry.user_id = self.user_id(entry)
                new_entry.user_name = self.user_name(entry)
                new_entry.rss_account = account
                new_entry.save()
                log.warning("{} {}".format(entry['id'], entry['published']))

    def link(self, entry):
        return entry.get('link') or entry.get('feedburner_origlink')

    def date(self, entry):
        if 'published_parsed' in entry:
            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
            dt.replace(tzinfo=utc)
            return dt
        return None

    def message(self, entry):
        if 'title' in entry:
            return entry.title
        
        return None

    def avatar(self, entry):
        if 'posterous_userimage' in entry:
            return entry.posterous_userimage
        
        return None
    
    def user_id(self, entry):
        return entry.get('posterous_profileurl') or entry.get('posterous_author')
    
    def user_name(self, entry):
        return entry.get('posterous_displayname')
    
    def blob(self, entry):
        return entry.summary if 'summary' in entry else json.dumps(entry)
        
    
