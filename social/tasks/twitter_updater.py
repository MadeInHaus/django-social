# import json
# from datetime import datetime
# import time
# import Queue
# import requests
# import logging
# from itertools import cycle
# from twython import Twython, TwythonError, TwythonRateLimitError, TwythonAuthError
# from urlparse import urlparse, parse_qs
# import gevent


# from .. import settings
# from ..models import TwitterAccount, TwitterSearch, TwitterMessage, TweetExistsError
# from ..settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET


# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class TwitterUpdater():
#     def __init__(self):
#         self.all_accounts = TwitterAccount.objects.all()
#         self.accounts = self._accounts_generator()
        
    
#     def _accounts_generator(self):
#         accounts = cycle(self.all_accounts)
#         while True:
#             a = next(accounts)
#             if not a.valid:
#                 accounts = [x for x in accounts if x.valid]
#                 if len(accounts) == 0:
#                     log.error('!!! ACCOUNTS EXHAUSTED !!!')
#                     raise StopIteration

#                 accounts = cycle(accounts)
#                 continue
#             yield a

    def update(self):
        pass
        
#         import gevent.monkey
#         gevent.monkey.patch_ssl()

#         self._update_account_timelines()
#         #self._update_search_terms()

        
#     def _update_account_timelines(self):
#         threads = []
#         for account in self.all_accounts:
#             if account.parse_timeline_tweets:
#                 threads.append(gevent.spawn(self._step_account, account))
#         gevent.joinall(threads)

#     def _update_search_terms(self):
#         threads = []
#         for term in TwitterSearch.objects.all():
#             threads.append(gevent.spawn(self._step, term))
#         gevent.joinall(threads)
    
#     def _step_account(self,account, page=0):
#         twitter = Twython(  app_key=SOCIAL_TWITTER_CONSUMER_KEY, 
#                                 app_secret=SOCIAL_TWITTER_CONSUMER_SECRET, 
#                                 oauth_token=account.oauth_token, 
#                                 oauth_token_secret=account.oauth_secret)
#         try:
#             log.warning('[twython account] ping account %s', account.screen_name)
#             log.warning('[twython account] page %s', page)
#             tweets = twitter.getUserTimeline(page=page,include_entities=True)
#         except TwythonRateLimitError:
#             log.error('[twython account error] hit twitter too much!  Switching accounts')
#             return
#         except TwythonAuthError:
#             log.error('[twython account error] account had some issues!')
#             return
#         except TwythonError as e:
#             log.error('[twitter account error] account-screenname:%s', account.screen_name)
#             log.error('[twitter account error] page:%s', page)
#             log.error('[twython account error] %s', e)
#             return
#         if len(tweets) == 0:
#             log.warning('[twitter account] no tweets for account %s on page %i',account.screen_name,page)
#             return
#         for tweet in tweets:
#             try:
#                 # create tweet and make sure it's unique based on id_str and search term
#                 dj_tweet = TwitterMessage.create_from_json(tweet,account=account)
#             except TweetExistsError:
#                 # item already exists, stop reading
#                 log.warning('[twitter account] kicking out (tweet exists)')
#                 return
#             except Exception as e:
#                 log.error('[twitter account] something went really wrong')
#                 log.error(e)
#                 return
        
#         self._step_account(account,page+1)

    



#     def _step(self, term, max_id=0):
        
#         try:
#             account = self.accounts.next()
#             twitter = Twython(  app_key=SOCIAL_TWITTER_CONSUMER_KEY, 
#                                 app_secret=SOCIAL_TWITTER_CONSUMER_SECRET, 
#                                 oauth_token=account.oauth_token, 
#                                 oauth_token_secret=account.oauth_secret)
#         except:
#             # no accounts, or they are all dead
#             log.error('[twitter] no valid twitter accounts to use')
#             return

#         try:
#             log.warning('[twitter] account-screenname:%s', account.screen_name)
#             log.warning('[twitter] search_term:%s', term.search_term)
#             log.warning('[twitter] max_id:%s', max_id)
#             response = twitter.search(q=term.search_term, count='100', max_id=max_id)
#             #gevent.sleep(0)
#         except TwythonRateLimitError:
#             log.error('[twython error] hit twitter too much!  Switching accounts')
#             account.valid = False
#             self._step(term,max_id)
#             return
#         except TwythonAuthError:
#             account.valid = False
#             log.error('[twython error] account had some issues!')
#             self._step(term,max_id)
#             return
#         except TwythonError as e:
#             account.valid = False
#             log.error('[twitter] account-screenname:%s', account.screen_name)
#             log.error('[twitter] search_term:%s', term.search_term)
#             log.error('[twitter] max_id:%s', max_id)
#             log.error('[twython error] %s', e)
#             self._step(term,max_id)
#             return
            
#         tweets = response.get('statuses',None)

#         if len(tweets) == 0:
#             log.warning('[twitter] no tweets for search term %s',term.search_term)
#             return
#         for tweet in tweets:
#             try:
#                 # create tweet and make sure it's unique based on id_str and search term
#                 dj_tweet = TwitterMessage.create_from_json(tweet, term)
#             except TweetExistsError:
#                 # item already exists, stop reading
#                 log.warning('[twitter] kicking out (tweet exists)')
#                 return
#             except Exception as e:
#                 log.error('something went really wrong')
#                 log.error(e)
#                 return
#             epoch = int(time.mktime(dj_tweet.date.timetuple()))
            
#             if epoch < term.search_until:
#                 # tweet was created before your limit, stop
#                 log.warning('[twitter] epoch: %s', epoch)
#                 log.warning('[twitter] search_until: %s', term.search_until)
#                 log.warning('[twitter] kicking out (tweet is too old)')
#                 return
            

#         # print(response.get('search_metadata'))
#         # sometimes the max_id_str was coming back empty... had to get it here instead
#         try:
#             search_meta = response.get('search_metadata', {})
#             max_id = self._get_max_id(search_meta)
#         except:
#             log.warning('[twitter] issues with twitter: %s', response.get('search_metadata'))
#             return
#         self._step(term,max_id=max_id)

#     def _get_max_id(self,search_metadata):
#         try:
#             max_id = parse_qs(urlparse(search_metadata.get('next_results')).query).get('max_id')
#             return max_id
#         except:
#             raise Exception

