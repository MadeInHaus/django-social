import requests


MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class RateLimitException(Exception): pass

class InstagramAPI(object):
    def __init__(self, account):
        self._account = account

    def _get_data_for_url(self, url):
        response = requests.get(url, params={
            'access_token': self._account.access_token,
        })

        if not response.ok and response.json()['error_type'] == 'OAuthRateLimitException':
            raise RateLimitException()
        else:
            return response

    def _retrieve_photos(self, url, max_photos):
        total_pictures = 0

        while url:
            response = self._get_data_for_url(url)
            print response.json()
            content = response.json()
            if not response.ok:
                raise RuntimeError(content['meta']['error_message'])

            url = content.get('pagination', {}).get('next_url')

            for photo in content.get('data', []):
                if total_pictures >= max_photos:
                    return
                else:
                    total_pictures += 1
                    yield photo

    def scrap_account(self, max_photos=100):
        url = 'https://api.instagram.com/v1/users/{}/media/recent/'.format(self._account.instagram_id)
        return self._retrieve_photos(url, max_photos)

    def search_tag(self, tag, max_photos=100):
        url = 'https://api.instagram.com/v1/tags/{}/media/recent'.format(tag)
        return self._retrieve_photos(url, max_photos)
