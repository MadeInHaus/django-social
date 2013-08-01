import sys
import time
import json

import feedparser

from time import mktime

from django.utils.datetime_safe import datetime
from django.utils.timezone import utc
from logging import getLogger
from bs4 import BeautifulSoup

from ..models import RSSMessage, RSSAccount


log = getLogger(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        elif type(obj) == time.struct_time:
            return datetime.fromtimestamp(time.mktime(obj)).isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

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
                new_entry.title = self.title(entry)
                new_entry.message = self.message(entry)
                new_entry.date = self.date(entry)
                new_entry.message_id = entry.id
                new_entry.deeplink = self.link(entry)
                new_entry.blob = self.blob(entry)
                new_entry.avatar = self.avatar(entry)
                new_entry.user_id = self.user_id(entry)
                new_entry.user_name = self.user_name(entry)
                new_entry.rss_account = account
                if new_entry.message:
                    new_entry.links = self.parse_links(new_entry.message)
                if new_entry.message:
                    new_entry.images = self.parse_images(new_entry.message)
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

    def title(self, entry):
        if 'title' in entry:
            return entry.title

        return None

    def message(self, entry):
        if 'summary' in entry:
            return entry.summary

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
        return json.dumps(entry, cls=JSONEncoder)

    def parse_links(self, message):
        try:
            soup = BeautifulSoup(message)
            links = soup.find_all('a')
            links = [s.prettify() for s in links]
        except:
            log.error("error parsing links: %s %s %s", *sys.exc_info())
            links = []

        return links

    def parse_images(self, message):
        try:
            soup = BeautifulSoup(message)
            images = soup.find_all('img')
            images = [{'src': s['src'], 'alt': s.get('alt',''), 'width': s.get('width', None), 'height': s.get('height', None)} for s in images]
        except:
            log.error("error parsing images: %s %s %s", *sys.exc_info())
            images = []

        return images
