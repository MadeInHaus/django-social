import requests
import json
import requests_oauthlib


MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class InstagramAPI(object):
    
    

    def __init__(self, app_id=None):
        self._app_id = app_id
        

    def _get_data_for_url(self,url, params=None):
        if not params:
            params = {}
        params['client_id'] = self._app_id
        resp = requests.get(url, params=params)
        return json.loads(resp.content)
    

    def tag_recent_media(self, tag, count=100):
        url = 'https://api.instagram.com/v1/tags/{}/media/recent'.format(tag)
        resp = self._get_data_for_url(url)
        total_sent = 0
        # if no meta or code isn't 200
        if not resp.get('meta',False) or resp.get('meta').get('code') != 200:
            raise Exception
            return

        while 1:
            messages = resp.get('data',[])
            if len(messages) == 0:
                raise StopIteration

            for message in messages:
                yield message
                total_sent += 1
                if total_sent >= count:
                    raise StopIteration
                
            try:
                pagination = resp.get('pagination')
                next_url = pagination.get('next_url')
            except KeyError:
                raise StopIteration

            resp = self._get_data_for_url(next_url)
            
        
