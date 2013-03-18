import requests
from requests_oauthlib import OAuth1
import json
from urlparse import parse_qs

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'

class TwitterAPI():

    def __init__(self,  client_key,
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
        oauth = OAuth1(self.client_key, client_secret=self.client_secret)
        req = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(req.content)
        obj = { 'resource_owner_key':credentials.get('oauth_token')[0],
                'resource_owner_secret':credentials.get('oauth_token_secret')[0],
                'auth_url':'https://api.twitter.com/oauth/authorize?oauth_token='\
                +credentials.get('oauth_token')[0]+'&oauth_callback='+self.callback_url
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

    def show_user(self,screen_name):
        url = 'https://api.twitter.com/1.1/users/show.json?screen_name={}'.format(screen_name)
        oauth = OAuth1(    
            self.client_key,
            client_secret=self.client_secret,
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret
        )

        
        account_info = requests.get(url=url, auth=oauth)

        return json.loads(account_info.content)

    def get_user_timeline(self):
        tmp = [x for x in range(10)]
        return tmp

# oauth = OAuth1('GB6gSL7mojCQK8lJe5JEg',client_secret='jhV32lskDKd4pZI9zDHsWrFXrQmakUApIGOANsd7g',resource_owner_key='Wd5S7bIpNj4XUNkC7lcwSPPpIZoPnfRW9HqmmqxOA0',resource_owner_secret='LzHNSkE4yl30siZVXST7qjOyguJEkgyrxOOzngQ',verifier='Wd5S7bIpNj4XUNkC7lcwSPPpIZoPnfRW9HqmmqxOA0')
# access_token_url = 'https://api.twitter.com/oauth/access_token'
# r = requests.post(url=access_token_url, auth=oauth)