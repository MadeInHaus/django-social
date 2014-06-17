import urllib
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'

class RateLimitException(Exception):
    def __init__(self, max_id=None):
        self.max_id = max_id
        super(RateLimitException, self).__init__()


class TwitterAPI():
    def __init__(self, client_key,
                       client_secret,
                       resource_owner_key=None,
                       resource_owner_secret=None,
                       verifier=None,
                       callback_url=None):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.verifier = verifier
        self.callback_url = callback_url

    def get_authentication_tokens(self):
        first_elem_or_empty_str = lambda dict_, key: key in dict_ and dict_[key][0] or ''
        oauth = OAuth1(self.client_key, client_secret=self.client_secret)
        req = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(req.content)
        obj = {
            'resource_owner_key': first_elem_or_empty_str(credentials, 'oauth_token'),
            'resource_owner_secret': first_elem_or_empty_str(credentials, 'oauth_token_secret'),
            'auth_url': ''.join([
                            'https://api.twitter.com/oauth/authorize?oauth_token=',
                            first_elem_or_empty_str(credentials, 'oauth_token'),
                            '&oauth_callback=',
                            self.callback_url,
            ]),
        }

        return obj


    def get_authorized_tokens(self):
        oauth = OAuth1(self.client_key,
                   client_secret=self.client_secret,
                   resource_owner_key=self.resource_owner_key,
                   resource_owner_secret=self.resource_owner_secret,
                   verifier=self.verifier)
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        req = requests.post(url=access_token_url, auth=oauth)
        credentials = parse_qs(req.content)
        authorized_tokens = {
            'oauth_token':credentials.get('oauth_token')[0],
            'oauth_token_secret':credentials.get('oauth_token_secret')[0],
            'screen_name':credentials.get('screen_name')[0],
            'user_id':credentials.get('user_id')[0],
        }

        self.resource_owner_key = credentials.get('oauth_token')[0]
        self.resource_owner_secret = credentials.get('oauth_token_secret')[0]

        return authorized_tokens

    def _get_obj_for_request(self, url, max_id=None):
        oauth = OAuth1(
            self.client_key,
            client_secret=self.client_secret,
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret
        )
        response = requests.get(url=url, auth=oauth)

        if response.reason == 'Too Many Requests':
            raise RateLimitException(max_id=max_id)
        response = response.json()
        return response


    def show_user(self, screen_name):
        url = 'https://api.twitter.com/1.1/users/show.json?screen_name={}'.format(screen_name)
        try:
            account_info = self._get_obj_for_request(url)
        except RateLimitException:
            raise
        return account_info

    def get_user_timeline(self, screen_name, max_count = 100):
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count={}'\
        .format(screen_name,max_count)
        tweets = self._get_obj_for_request(url)
        total_sent = 0
        while 1:
            if len(tweets) == 0:
                raise StopIteration

            for tweet in tweets:
                total_sent += 1
                if(max_count != 0 and total_sent > max_count):
                    raise StopIteration
                yield tweet

            page_url = url + '&max_id=' + tweet['id_str']
            tweets = self._get_obj_for_request(page_url)


    def search(self, search_term, max_count=100, max_id=None):
        search_term = urllib.quote(search_term)
        url = 'https://api.twitter.com/1.1/search/tweets.json?count=100&result_type=mixed&q={}'.format(search_term)
        response = self._get_obj_for_request(url)
        tweets = response.get('statuses', [])
        total_sent = 0
        while 1:
            if len(tweets) == 0:
                raise StopIteration
            for tweet in tweets:
                total_sent += 1
                if(max_count != 0 and total_sent > max_count):
                    raise StopIteration
                yield tweet
            max_id = str(tweet['id'] - 1)

            page_url = url + '&max_id=' + max_id
            response = self._get_obj_for_request(page_url, max_id=max_id)
            tweets = response.get('statuses', [])
            # twitter responds back including the item 'max_id' have to pop it out
