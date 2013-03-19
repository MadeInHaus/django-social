import os
import json
import time
from datetime import datetime
from .. import settings
from ..tasks.twitter_updater import TwitterUpdater
from ..models import TwitterAccount, TwitterMessage, TwitterSearch, TweetExistsError
from ..services.twitter import TwitterAPI, RateLimitException

from django.test import TestCase
from ConfigParser import RawConfigParser


config = RawConfigParser()
config.read(os.getcwd()+'/project/apps/social/tests/resources/config.ini')


class TwitterTest(TestCase):
    
    def setUp(self):
        pass       
        

    def test_twitter_api_get_authentication_tokens(self):
        twapi = TwitterAPI( 
            settings.SOCIAL_TWITTER_CONSUMER_KEY, 
            settings.SOCIAL_TWITTER_CONSUMER_SECRET,
            callback_url='http://www.google.com')
        obj = twapi.get_authentication_tokens()
        self.assertTrue(obj)
        self.assertTrue(obj['auth_url'])
        self.assertTrue(obj['resource_owner_secret'])
        self.assertTrue(obj['resource_owner_key'])

    
    def test_twitter_api_show_user(self):
        twapi = TwitterAPI( 
            client_key = settings.SOCIAL_TWITTER_CONSUMER_KEY, 
            client_secret = settings.SOCIAL_TWITTER_CONSUMER_SECRET,
            resource_owner_key = config.get('twitter', 'RESOURCE_OWNER_KEY'),
            resource_owner_secret = config.get('twitter', 'RESOURCE_OWNER_SECRET')
        )
        account_info = twapi.show_user(config.get('twitter', 'USERNAME'))
        self.assertTrue(account_info)
        twaccount = TwitterAccount.create_from_obj(
            account_info, 
            oauth_token=config.get('twitter', 'RESOURCE_OWNER_KEY'), 
            oauth_token_secret=config.get('twitter', 'RESOURCE_OWNER_SECRET')
        )
        self.assertTrue(twaccount.id)
        
        


    def test_twitter_api_get_user_timeline(self):
        obj = {u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 295947098, u'verified': False, u'profile_text_color': u'333333', u'profile_image_url_https': u'https://si0.twimg.com/profile_images/1688391755/image_normal.jpg', u'profile_sidebar_fill_color': u'DDEEF6', u'entities': {u'description': {u'urls': []}}, u'followers_count': 32, u'profile_sidebar_border_color': u'C0DEED', u'id_str': u'295947098', u'profile_background_color': u'C0DEED', u'listed_count': 3, u'status': {u'lang': u'en', u'favorited': False, u'entities': {u'user_mentions': [{u'id': 229709694, u'indices': [49, 59], u'id_str': u'229709694', u'screen_name': u'Prismatic', u'name': u'Prismatic'}], u'hashtags': [], u'urls': [{u'url': u'http://t.co/IQVuabOr3a', u'indices': [22, 44], u'expanded_url': u'http://prsm.tc/PBXRTt', u'display_url': u'prsm.tc/PBXRTt'}]}, u'contributors': None, u'truncated': False, u'text': u'Getting Into Ember.js http://t.co/IQVuabOr3a via @prismatic', u'created_at': u'Fri Mar 15 13:43:43 +0000 2013', u'retweeted': False, u'in_reply_to_status_id_str': None, u'coordinates': None, u'in_reply_to_user_id_str': None, u'source': u'<a href="http://getprismatic.com" rel="nofollow">getprismatic.com</a>', u'in_reply_to_status_id': None, u'in_reply_to_screen_name': None, u'id_str': u'312559738472783872', u'place': None, u'retweet_count': 0, u'geo': None, u'id': 312559738472783872L, u'possibly_sensitive': False, u'in_reply_to_user_id': None}, u'profile_background_image_url_https': u'https://si0.twimg.com/images/themes/theme1/bg.png', u'utc_offset': None, u'statuses_count': 402, u'description': u'', u'friends_count': 17, u'location': u'', u'profile_link_color': u'0084B4', u'profile_image_url': u'http://a0.twimg.com/profile_images/1688391755/image_normal.jpg', u'following': False, u'geo_enabled': False, u'profile_banner_url': u'https://si0.twimg.com/profile_banners/295947098/1358746251', u'profile_background_image_url': u'http://a0.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'dinopetrone', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 5, u'name': u'dino petrone', u'notifications': False, u'url': None, u'created_at': u'Mon May 09 22:59:55 +0000 2011', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'default_profile': True, u'is_translator': False}
        account = TwitterAccount.create_from_obj(obj, 1234, 1234)
        # RUN THIS TEST BY PUTTING IN A VALID KEY/SECRET
        twapi = TwitterAPI( 
            client_key = settings.SOCIAL_TWITTER_CONSUMER_KEY, 
            client_secret = settings.SOCIAL_TWITTER_CONSUMER_SECRET,
            resource_owner_key = config.get('twitter', 'RESOURCE_OWNER_KEY'),
            resource_owner_secret = config.get('twitter', 'RESOURCE_OWNER_SECRET')
        )
        tweets = twapi.get_user_timeline(config.get('twitter', 'USERNAME'),max_count=10)
        try:
            for tweet in tweets:
                try:
                    dj_tweet = TwitterMessage.create_from_json(tweet,account=account)
                except TweetExistsError:
                    pass
        except RateLimitException:
            pass
        except Exception:
            pass
        self.assertTrue(dj_tweet)
        tweets = TwitterMessage.objects.all()
        self.assertEqual(len(tweets),10)
        

    def test_twitter_api_search(self):
        TEST_COUNT = 50
        twapi = TwitterAPI( 
            client_key = settings.SOCIAL_TWITTER_CONSUMER_KEY, 
            client_secret = settings.SOCIAL_TWITTER_CONSUMER_SECRET,
            resource_owner_key = config.get('twitter', 'RESOURCE_OWNER_KEY'),
            resource_owner_secret = config.get('twitter', 'RESOURCE_OWNER_SECRET')
        )
        tweets = twapi.search('#test',max_count=TEST_COUNT)
        total_duplicates = 0
        tweet_duplicate = 0
        try:
            for tweet in tweets:
                try:
                    dj_tweet = TwitterMessage.create_from_json(tweet)
                    tweet_duplicate = 0
                except TweetExistsError as e:
                    tweet_duplicate += 1
                    total_duplicates += 1
                    if tweet_duplicate > 5:
                        print('5 in a row')
                        return
        except RateLimitException as e:
            print(e.max_id)
            print('limit')
        
        tweets = TwitterMessage.objects.all()
        self.assertEqual(len(tweets)+total_duplicates, TEST_COUNT)

        
    def test_twitter_model_account_create_from_obj(self):
        obj = {u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 295947098, u'verified': False, u'profile_text_color': u'333333', u'profile_image_url_https': u'https://si0.twimg.com/profile_images/1688391755/image_normal.jpg', u'profile_sidebar_fill_color': u'DDEEF6', u'entities': {u'description': {u'urls': []}}, u'followers_count': 32, u'profile_sidebar_border_color': u'C0DEED', u'id_str': u'295947098', u'profile_background_color': u'C0DEED', u'listed_count': 3, u'status': {u'lang': u'en', u'favorited': False, u'entities': {u'user_mentions': [{u'id': 229709694, u'indices': [49, 59], u'id_str': u'229709694', u'screen_name': u'Prismatic', u'name': u'Prismatic'}], u'hashtags': [], u'urls': [{u'url': u'http://t.co/IQVuabOr3a', u'indices': [22, 44], u'expanded_url': u'http://prsm.tc/PBXRTt', u'display_url': u'prsm.tc/PBXRTt'}]}, u'contributors': None, u'truncated': False, u'text': u'Getting Into Ember.js http://t.co/IQVuabOr3a via @prismatic', u'created_at': u'Fri Mar 15 13:43:43 +0000 2013', u'retweeted': False, u'in_reply_to_status_id_str': None, u'coordinates': None, u'in_reply_to_user_id_str': None, u'source': u'<a href="http://getprismatic.com" rel="nofollow">getprismatic.com</a>', u'in_reply_to_status_id': None, u'in_reply_to_screen_name': None, u'id_str': u'312559738472783872', u'place': None, u'retweet_count': 0, u'geo': None, u'id': 312559738472783872L, u'possibly_sensitive': False, u'in_reply_to_user_id': None}, u'profile_background_image_url_https': u'https://si0.twimg.com/images/themes/theme1/bg.png', u'utc_offset': None, u'statuses_count': 402, u'description': u'', u'friends_count': 17, u'location': u'', u'profile_link_color': u'0084B4', u'profile_image_url': u'http://a0.twimg.com/profile_images/1688391755/image_normal.jpg', u'following': False, u'geo_enabled': False, u'profile_banner_url': u'https://si0.twimg.com/profile_banners/295947098/1358746251', u'profile_background_image_url': u'http://a0.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'dinopetrone', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 5, u'name': u'dino petrone', u'notifications': False, u'url': None, u'created_at': u'Mon May 09 22:59:55 +0000 2011', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'default_profile': True, u'is_translator': False}
        TwitterAccount.create_from_obj(obj, 1234, 1234)
        twa = TwitterAccount.objects.all()[0]
        self.assertEqual(twa.twitter_id, 295947098)
        self.assertEqual(twa.screen_name, 'dinopetrone')
        self.assertEqual(twa.profile_image_url_https, u'https://si0.twimg.com/profile_images/1688391755/image_normal.jpg')
        self.assertEqual(twa.verified, False)
        self.assertEqual(twa.oauth_token, u'1234')
        self.assertEqual(twa.oauth_secret, u'1234')

    def test_twitter_model_message_create_from_json(self):
        with open(os.getcwd()+'/project/apps/social/tests/resources/twitter_multi_insert.json') as f:
            tweets = json.loads(f.read())
        for tweet in tweets:
            created_tweet = TwitterMessage.create_from_json(tweet)
            break

        self.assertEqual(created_tweet.deeplink, 'https://twitter.com/dinopetrone/status/312559738472783872')
        self.assertEqual(created_tweet.message, 'Getting Into Ember.js http://t.co/IQVuabOr3a via @prismatic')
        self.assertEqual(created_tweet.user_id, '312559738472783872')
        self.assertEqual(created_tweet.network, 'twitter')
        self.assertEqual(created_tweet.retweeted, False)
        self.assertEqual(created_tweet.source, '<a href="http://getprismatic.com" rel="nofollow">getprismatic.com</a>')
        self.assertEqual(created_tweet.user_name, 'dinopetrone')
        self.assertEqual(created_tweet.message_id, '312559738472783872')
        self.assertEqual(created_tweet.status, 1)
        self.assertEqual(created_tweet.favorited, False)
        self.assertEqual(created_tweet.avatar, 'https://si0.twimg.com/profile_images/1688391755/image_normal.jpg')
        self.assertEqual(created_tweet.message_type, 'post')
        




            
