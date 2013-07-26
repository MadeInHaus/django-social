import time
from .. import settings
import requests
from ..models import FacebookAccount, FacebookMessage
from celery.utils.log import get_task_logger
from urlparse import urlparse, parse_qs


log = get_task_logger('facebook')


class FacebookUpdater(object):
    def __init__(self, api):
        self.fbapi = api

    def update(self):
        facebookAccounts = FacebookAccount.objects.all()
        for account in facebookAccounts:
            messages = self.fbapi.get_feed_for_account(account)
            for message in messages:
                FacebookMessage.create_from_json(account, message)

            account.last_poll_time = int(time.time())
            account.save()