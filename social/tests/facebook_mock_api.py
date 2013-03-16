import os
import json
import requests

class FacebookAPISingleInsert(object):
    def __init__(self, app_id, app_secret):
        pass

    def get_feed_for_account(self,account):
        with open(os.getcwd()+'/project/apps/social/tests/resources/facebook_single_instert.json') as f:
            j = json.loads(f.read())
            return j['data']

            
class FacebookAPIMultiInstert(object):
    def __init__(self, app_id, app_secret):
        pass

    def get_feed_for_account(self,account):
        with open(os.getcwd()+'/project/apps/social/tests/resources/facebook_multi_insert.json') as f:
            j = json.loads(f.read())
            return j['data']

            
