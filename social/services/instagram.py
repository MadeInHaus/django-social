import requests
import json
import requests_oauthlib


MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class InstagramAPI(object):
    def __init__(self, app_id=None):
        self._app_id = app_id

    def _get_data_for_url(self, url, params={}):
        params['client_id'] = self._app_id
        return requests.get(url, params=params)

    def tag_recent_media(self, tag, count=100):
        url = 'https://api.instagram.com/v1/tags/{}/media/recent'.format(tag)
        total_sent = 0

        while url:
            res = self._get_data_for_url(url)
            content = res.json()
            if not res.ok:
                raise RuntimeError(content['meta']['error_message'])

            messages = content.get('data', [])

            for message in messages:
                yield message
                total_sent += 1
                if total_sent >= count:
                    raise StopIteration()

            url = content.get('pagination', {}).get('next_url')
