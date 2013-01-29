from .. import settings
import requests
from ..models import FacebookAccount

class FacebookUpdater():
    def __init__(self):
        self._access_token = None
        self._app_id = settings.SOCIAL_FACEBOOK_APP_ID
        self._app_secret = settings.SOCIAL_FACEBOOK_APP_SECRET

    def __new__(self):
        self._get_access_token()

    def _get_access_token(self):
        url = 'https://graph.facebook.com/oauth/access_token?\
            client_id={0}&\
            client_secret={1}&\
            grant_type=client_credentials'.format(self._app_id, self._app_secret)

        r = requests.get(url)
        self._access_token = r.text.split('=')[1];

    def update(self):
        #to get the id
        #http://graph.facebook.com/dinopetrone
        
        facebookAccounts = FacebookAccount.objects.all()
        for account in facebookAccounts:
            print(account.fb_id)
        # url = "https://graph.facebook.com/{0}/feed?access_token={1}&filter=2&since={2}".\
        #                             format(fb_account.id, self._access_token, 0)
        # r = requests.get(url)
