import requests


MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class RateLimitException(Exception): pass

def _get_data_for_url(url, client_id=None, access_token=None):
    params = {}
    if client_id:
        params['client_id'] = client_id
    if access_token:
        params['access_token'] = access_token

    response = requests.get(url, params=params)

    if not response.ok:
        print "Bad response, got this:\n{}".format(response.content)

    if not response.ok and response.json()['error_type'] == 'OAuthRateLimitException':
        raise RateLimitException()
    else:
        return response

def _retrieve_photos(url, max_photos, client_id=None, access_token=None):
    total_pictures = 0

    while url:
        response = _get_data_for_url(url, client_id=client_id, access_token=access_token)
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


class InstagramPublicAPI(object):
    def __init__(self, instagram_setting):
        self._client_id = instagram_setting.client_id

    def get_id_from_username(self, username):
        url = 'https://api.instagram.com/v1/users/search?q={}&client_id={}'.format(username, self._client_id)
        r = requests.get(url)
        return int(r.json()['data'][0]['id'])

    def scrape_public_account(self, account, max_photos=100):
        url = 'https://api.instagram.com/v1/users/{}/media/recent/'.format(account.instagram_id)
        return _retrieve_photos(url, max_photos, client_id=self._client_id)

    def search_tag(self, tag, max_photos=100):
        if tag.username:
            url = 'https://api.instagram.com/v1/users/{}/media/recent/'.format(tag.instagram_id)
        else:
            url = 'https://api.instagram.com/v1/tags/{}/media/recent'.format(tag.search_term)

        if tag.last_id:
            url = '{}?min_id={}'.format(url, tag.last_id)

        return _retrieve_photos(url, max_photos, client_id=self._client_id)


class InstagramAPI(object):
    def __init__(self, account):
        self._account = account

    def scrape_account(self, max_photos=100):
        url = 'https://api.instagram.com/v1/users/{}/media/recent/'.format(self._account.instagram_id)
        return _retrieve_photos(url, max_photos, access_token=self._account.access_token)

    def search_tag(self, tag, max_photos=100):
        if tag.username:
            url = 'https://api.instagram.com/v1/users/{}/media/recent/'.format(tag.instagram_id)
        else:
            url = 'https://api.instagram.com/v1/tags/{}/media/recent'.format(tag.search_term)

        if tag.last_id:
            url = '{}?min_id={}'.format(url, tag.last_id)

        return _retrieve_photos(url, max_photos, access_token=self._account.access_token)

