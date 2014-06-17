import time
from ..models import FacebookAccount, FacebookMessage, FacebookSearch, FacebookPublicAccount
from celery.utils.log import get_task_logger


log = get_task_logger('facebook')

class FacebookUpdater(object):
    def __init__(self, api):
        self.fbapi = api

    def update(self):
        facebookAccounts = FacebookAccount.objects.all()
        for account in facebookAccounts:
            messages = self.fbapi.get_feed_for_account(account)
            for message in messages:
                FacebookMessage.create_from_json(message, account)

            account.last_poll_time = int(time.time())
            account.save()

        facebookAccounts = FacebookPublicAccount.objects.all()
        for account in facebookAccounts:
            messages = self.fbapi.get_feed_for_account(account)
            for message in messages:
                FacebookMessage.create_from_json(message, account)

            account.last_poll_time = int(time.time())
            account.save()


        for query in FacebookSearch.objects.all():
            messages = self.fbapi.get_search(query)
            for message in messages:
                FacebookMessage.create_from_json(message)

            query.last_poll_time = int(time.time())
            query.save()
