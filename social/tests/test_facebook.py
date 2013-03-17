import os
import json
import time
from datetime import datetime
from .. import settings
from ..tasks.facebook_updater import FacebookUpdater
from .facebook_mock_api import FacebookAPISingleInsert, FacebookAPIMultiInstert
from ..models import FacebookAccount, FacebookMessage
from ..services.facebook import FacebookAPI

from django.test import TestCase
import logging


class FacebookTest(TestCase):
    
    def setUp(self):
        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        fba = FacebookAccount()
        fba.fb_id = 'asdf'
        fba.save()
        self.fba = fba

    def test_facebook_update(self):
        fbapi = FacebookAPISingleInsert(
            settings.SOCIAL_FACEBOOK_APP_ID,
            settings.SOCIAL_FACEBOOK_APP_SECRET)
        fb = FacebookUpdater(fbapi)
        fb.update()

        messages = list(FacebookMessage.objects.all())
        self.assertTrue(len(messages) > 0)
    
    def test_facebook_create_from_json(self):
        with open(os.getcwd()+'/project/apps/social/tests/resources/facebook_single_instert.json') as f:
            j = json.loads(f.read())
            data = j['data'][0]


        FacebookMessage.create_from_json(self.fba, data)
        messages = list(FacebookMessage.objects.all())
        message = messages[0]
        self.assertEqual(message.facebook_account, self.fba)
        self.assertEqual(message.message_type, 'post')
        self.assertEqual(message.message, 'message')
        self.assertEqual(message.avatar, 'https://graph.facebook.com/12345/picture')
        self.assertEqual(message.user_id, '12345')
        self.assertEqual(message.user_name, 'dino')
        self.assertEqual(int(time.mktime(message.date.timetuple())*1000), 1362780116000)
        self.assertEqual(message.message_id, '11936081183_539182919435428')
        self.assertEqual(message.deeplink, u'https://www.facebook.com/11936081183/posts/539182919435428')
        self.assertEqual(message.blob,  u"{u'from': {u'name': u'dino', u'id': u'12345'}, u'name': u'GMO Labeling Coming to Whole Foods Market', u'privacy': {u'value': u''}, u'description': u'Whole Foods Market commits to full GMO transparency by giving supplier partners five years to source non-GMO ingredients or to clearly label products with ingredients containing GMOs. Today, we stood up for the consumer\\u2019s right to know by announcing that all products in our US and Canadian stores co...', u'comments': {u'count': 1, u'data': [{u'created_time': u'2013-03-09T18:35:08+0000', u'message': u'Naked will finally have to be labeled as GMO. Also the other products will too.', u'from': {u'name': u'Jase Mill', u'id': u'100001732030174'}, u'id': u'11936081183_539182919435428_6135207', u'likes': 2}]}, u'updated_time': u'2013-03-09T18:35:08+0000', u'caption': u'www.wholefoodsmarket.com', u'link': u'http://www.wholefoodsmarket.com/blog/gmo-labeling-coming-whole-foods-market?utm_medium=Any_Social_Media&utm_source=SocialMedia&utm_campaign=GMO_Labeling', u'likes': {u'count': 2, u'data': [{u'name': u'Benjamin Steineman', u'id': u'645033899'}, {u'name': u'John Connor', u'id': u'100005033045141'}]}, u'created_time': u'2013-03-08T22:01:56+0000', u'message': u'message', u'type': u'status', u'id': u'11936081183_539182919435428', u'to': {u'data': [{u'category': u'Food/beverages', u'name': u'Naked Juice', u'id': u'11936081183'}]}, u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif'}")

    #tries to insert 22 items (last 2 are duplicates)
    def test_facebook_ensure_no_duplicates(self):
        fbapi = FacebookAPIMultiInstert(
            settings.SOCIAL_FACEBOOK_APP_ID,
            settings.SOCIAL_FACEBOOK_APP_SECRET)
        fb = FacebookUpdater(fbapi)
        fb.update()

        messages = list(FacebookMessage.objects.all())
        self.assertEqual(len(messages),20)

    