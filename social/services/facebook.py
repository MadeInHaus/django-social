import requests

import logging
log = logging.getLogger(__name__)

def get_id_from_username(username):
    url = 'http://graph.facebook.com/{}'.format(username)
    r = requests.get(url)
    return r.json()['id']

def get_username_from_id(fb_id):
    url = 'http://graph.facebook.com/{}'.format(fb_id)
    r = requests.get(url)
    return r.json()['username']


class FacebookAPI(object):
    def __init__(self, app_id, app_secret):
        self._app_id = app_id
        self._app_secret = app_secret
        self._access_token = None
        self._get_access_token()

    def _get_data_for_url(self, url):
        data = requests.get(url)
        return data.json()

    def _get_access_token(self):
        if self._app_id and self._app_secret:
            url = 'https://graph.facebook.com/oauth/access_token?' \
                  'client_id={0}&' \
                  'client_secret={1}&' \
                  'grant_type=client_credentials'.format(self._app_id, self._app_secret)

            r = requests.get(url)
            self._access_token = r.text.split('=')[1];

    def get_feed_for_account(self, account):
        if self._access_token:
            url = "https://graph.facebook.com/{0}/feed?access_token={1}&filter=2&since={2}"\
                      .format(account.get_id(), self._access_token, account.last_poll_time)
            while url:
                data = self._get_data_for_url(url)
                messages = data.get('data', [])

                for item in messages:
                    yield item

                url = data.get('paging', {}).get('next')

    def get_photo_data(self, msg):
        if not 'object_id' in msg:
            return None
        url = "https://graph.facebook.com/{}?access_token={}"
        data = self._get_data_for_url(url.format(msg['object_id'], self._access_token))
        return data

    def get_search(self, query):
        if self._access_token:
            url = "https://graph.facebook.com/search?access_token={0}&q={1}&type=post&since={2}"\
                      .format(self._access_token, query.search_term, query.last_poll_time)
            while url:
                print url
                data = self._get_data_for_url(url)
                messages = data.get('data', [])

                for item in messages:
                    yield item

                url = data.get('paging', {}).get('previous')
