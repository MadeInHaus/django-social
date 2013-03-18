import requests
import json

class FacebookAPI(object):
    def __init__(self, app_id, app_secret):
        self._app_id = app_id
        self._app_secret = app_secret
        self._access_token = None
        self._get_access_token()

    def _get_data_for_url(self,url):
        data = requests.get(url)
        return data.json

    def _get_access_token(self):
        url =   'https://graph.facebook.com/oauth/access_token?\
                client_id={0}&\
                client_secret={1}&\
                grant_type=client_credentials'.format(self._app_id, self._app_secret)
        
        r = requests.get(url)
        self._access_token = r.text.split('=')[1];
    
    def get_feed_for_account(self,account):
        url = "https://graph.facebook.com/{0}/feed?access_token={1}&filter=2&since={2}"\
                                        .format(account.fb_id, self._access_token, account.last_poll_time)
        data = self._get_data_for_url(url)
        
        while 1:
            messages = data.get('data', [])

            if len(messages) == 0:
                raise StopIteration
            
            for item in messages:
                yield item

            try:
                next_url = data['paging']['next']
            except KeyError:
                raise StopIteration

            data = self._get_data_for_url(next_url)
            messages = data.get('data', [])
            
