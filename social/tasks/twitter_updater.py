import logging
import gevent

from itertools import cycle

from .. import settings
from ..models import TwitterAccount, TwitterSearch, TwitterMessage, TweetExistsError, TwitterPublicAccount
from ..services.twitter import TwitterAPI, RateLimitException

MAX_DUPLICATES = 20


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TwitterUpdater():
    def __init__(self):
        self.all_accounts = TwitterAccount.objects.all()
        self.public_accounts = TwitterPublicAccount.objects.all()
        self.accounts = self._accounts_generator()

    def _accounts_generator(self):
        accounts = cycle(self.all_accounts)
        while True:
            a = next(accounts)
            if not a.valid:
                accounts = [x for x in accounts if x.valid]
                if len(accounts) == 0:
                    log.error('!!! ACCOUNTS EXHAUSTED !!!')
                    raise StopIteration

                accounts = cycle(accounts)
                continue
            yield a

    def update(self):
        import gevent.monkey
        gevent.monkey.patch_ssl()

        self._update_account_timelines()
        self._update_search_terms()

    def _update_search_terms(self):
        threads = []
        for term in TwitterSearch.objects.all():
            threads.append(gevent.spawn(self._update_search_term, term))
        gevent.joinall(threads)

    def _update_account_timelines(self):
        threads = []
        for account in list(self.all_accounts) + list(self.public_accounts):
            if account.parse_timeline_tweets:
                threads.append(gevent.spawn(self._update_account_timeline, account))
        gevent.joinall(threads)

    def _api_from_account(self,account):
        if type(account) != TwitterAccount:
            account = None

        twapi = TwitterAPI(
            client_key = settings.SOCIAL_TWITTER_CONSUMER_KEY,
            client_secret = settings.SOCIAL_TWITTER_CONSUMER_SECRET,
            resource_owner_key = account.oauth_token if account else None,
            resource_owner_secret = account.oauth_secret if account else None)
        return twapi

    def _refresh_api_with_new_account(self, api, account):
        pass


    def _update_account_timeline(self, account):
        twapi = self._api_from_account(account)
        tweets = twapi.get_user_timeline(account.screen_name, max_count=0)
        log.warning('[twitter account] ping account: %s', account.screen_name)
        try:
            for tweet in tweets:
                try:
                    _dj_tweet = TwitterMessage.create_from_json(tweet,account=account)
                except TweetExistsError:
                    return
        except RateLimitException:
            log.warning('[twitter] rate limit exceeded')

        except Exception as e:
            log.warning('[twitter] big problem: %s', e)

    def _update_public_account_timeline(self, account):
        twapi = self._api_from_account(account)
        tweets = twapi.get_user_timeline(account.username, max_count=0)
        log.warning('[twitter account] ping account: %s', account.username)
        try:
            for tweet in tweets:
                try:
                    dj_tweet = TwitterMessage.create_from_json(tweet,account=account)
                except TweetExistsError:
                    return
        except RateLimitException:
            log.warning('[twitter] rate limit exceeded')

        except Exception as e:
            log.warning('[twitter] big problem: %s', e)


    def _update_search_term(self, term, max_id=None):
        try:
            account = self.accounts.next()
        except StopIteration:
            log.warning('Problem iterating accounts?  Proceeding with account=None')
            account = None
        twapi = self._api_from_account(account)
        tweets = twapi.search(term.search_term, max_count=0)
        tweet_duplicate = 0
        try:
            for tweet in tweets:
                try:
                    dj_tweet = TwitterMessage.create_from_json(tweet)
                except TweetExistsError:
                    tweet_duplicate += 1
                    if tweet_duplicate > MAX_DUPLICATES:
                        log.warning('[twitter] you hit {} duplicates in a row, kicking out'.format(MAX_DUPLICATES))
                        return

        except RateLimitException as e:
            account.valid = False
            print('*******************')
            print(e.max_id)
            self._update_search_term(term, e.max_id)
