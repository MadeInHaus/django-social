import os
import requests
import json
from .. import settings
from ..models import InstagramSearch, InstagramMessage, IGMediaExistsError
from ..services.instagram import InstagramAPI
from django.test import TestCase



class InstagramTest(TestCase):

    def setUp(self):
        term = InstagramSearch()
        term.search_term = 'pie'
        term.save()

    def test_instagram_api_tag_recent_media(self):
        api = InstagramAPI( app_id=settings.SOCIAL_INSTAGRAM_CLIENT_ID)
        COUNT = 10000
        messages = api.tag_recent_media('cake', count=COUNT)
        term = InstagramSearch.objects.all()[0]

        for message in messages:
            try:
                ig_media = InstagramMessage.create_from_json(message,term)
            except IGMediaExistsError as e:
                print('duplicate error')
                pass
            except Exception as e:
                log.error('[instagrame] larger problem...')
                log.error(e)
            
        dj_msgs = InstagramMessage.objects.all()
        self.assertEqual(len(dj_msgs),COUNT)

    def test_instagram_model_message_create(self):
        
        with open(os.getcwd()+'/project/apps/social/tests/resources/instagram_single_insert.json') as f:
            message = json.loads(f.read())
        
        term = InstagramSearch.objects.all()[0]
        ig_media = InstagramMessage.create_from_json(message,term)

        self.assertEqual(ig_media.status , 1)
        self.assertEqual(ig_media.reply_to_id , None)
        self.assertEqual(ig_media.user_id , '49051814')
        self.assertEqual(ig_media.network , 'instagram')
        self.assertEqual(ig_media.user_name , 'djlalive')
        self.assertEqual(ig_media.deeplink , 'http://instagr.am/p/XC9FhxHF7U/')
        self.assertEqual(ig_media.message_id , '415162776363491028_49051814')
        self.assertEqual(ig_media.message , 'New addition to the family MIA #Uncle @mommy_2_mia13')
        self.assertEqual(ig_media.message_type , 'post')
        self.assertEqual(ig_media.avatar , 'http://images.instagram.com/profiles/profile_49051814_75sq_1363174949.jpg')

    