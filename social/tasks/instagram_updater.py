import time
from .. import settings

#from ..models import FacebookAccount, FacebookMessage
from celery.utils.log import get_task_logger
from instagram.client import InstagramAPI

log = get_task_logger(__name__)


class InstagramUpdater():
    def __init__(self):
        self._access_token = None
        self._app_id = settings.SOCIAL_INSTAGRAM_CLIENT_ID
        self._app_secret = settings.SOCIAL_INSTAGRAM_CLIENT_SECRET
        
        # self.api = InstagramAPI(client_id=settings.SOCIAL_INSTAGRAM_CLIENT_ID,
        #                         client_secret=settings.SOCIAL_INSTAGRAM_CLIENT_SECRET,
        #                         redirect_uri='http://127.0.0.1:8000')
        # token, user = api.exchange_code_for_access_token(code)



    def update(self):
        pass
        # response = self.api.tag_search('#face')
        # print(response)
        