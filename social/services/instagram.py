import gevent
import requests


MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class RateLimitException(Exception): pass

class InstagramAPI(object):
    def __init__(self, app_id=None):
        self._app_id = app_id

    def _scrap_accounts(self):
        threads = []

        for account in self.accounts:
            if account.scrap_profile:
                threads.append(gevent.spawn(self._scrap_account, account))

        gevent.joinall(threads)

    def _scrap_account(self, account, max_photos=100):
        url = 'https://api.instagram.com/v1/users/3/media/recent/' \
              '?access_token={}'.format(account.access_token)
        total_pictures = 0

        while url:
            response = self._get_data_for_url(url)
            content = response.json()
            url = content.get('pagination', {}).get('next_url')

            for photo in content['data']:
                if total_pictures > max_photos:
                    return
                else:
                    total_pictures += 1
                    yield photo

    def _get_data_for_url(self, url, params={}):
        params['client_id'] = self._app_id
        response = requests.get(url, params=params)

        if not response.ok and response.json()['error_type'] == 'OAuthRateLimitException':
            raise RateLimitException()
        else:
            return response

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
