# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FacebookMessage.facebook_public_account'
        db.add_column(u'social_facebookmessage', 'facebook_public_account',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.FacebookPublicAccount'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FacebookMessage.facebook_public_account'
        db.delete_column(u'social_facebookmessage', 'facebook_public_account_id')


    models = {
        u'social.facebookaccount': {
            'Meta': {'object_name': 'FacebookAccount'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poll_time': ('django.db.models.fields.IntegerField', [], {'default': '1403031384'})
        },
        u'social.facebookmessage': {
            'Meta': {'object_name': 'FacebookMessage', '_ormbases': [u'social.Message']},
            'facebook_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookAccount']", 'null': 'True', 'blank': 'True'}),
            'facebook_public_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookPublicAccount']", 'null': 'True', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'social.facebookpublicaccount': {
            'Meta': {'object_name': 'FacebookPublicAccount'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poll_time': ('django.db.models.fields.IntegerField', [], {'default': '1403031384'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'social.facebooksearch': {
            'Meta': {'object_name': 'FacebookSearch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poll_time': ('django.db.models.fields.IntegerField', [], {'default': '1403031384'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'})
        },
        u'social.facebooksetting': {
            'Meta': {'object_name': 'FacebookSetting'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filter_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_photo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        },
        u'social.instagramaccount': {
            'Meta': {'object_name': 'InstagramAccount'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'scrap_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'social.instagrammessage': {
            'Meta': {'object_name': 'InstagramMessage', '_ormbases': [u'social.Message']},
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'images': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'instagram_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['social.InstagramSearch']", 'null': 'True', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'social.instagrampublicaccount': {
            'Meta': {'object_name': 'InstagramPublicAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'social.instagramsearch': {
            'Meta': {'object_name': 'InstagramSearch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'})
        },
        u'social.instagramsetting': {
            'Meta': {'object_name': 'InstagramSetting'},
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'social.message': {
            'Meta': {'object_name': 'Message'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blob': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'deeplink': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20', 'db_index': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'reply_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reply'", 'null': 'True', 'to': u"orm['social.Message']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'social.rssaccount': {
            'Meta': {'object_name': 'RSSAccount'},
            'feed_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'social.rssmessage': {
            'Meta': {'object_name': 'RSSMessage', '_ormbases': [u'social.Message']},
            '_images': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            '_links': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'rss_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.RSSAccount']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'social.rsssetting': {
            'Meta': {'object_name': 'RSSSetting'},
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        },
        u'social.twitteraccount': {
            'Meta': {'object_name': 'TwitterAccount'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'entities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parse_timeline_tweets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poll_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile_background_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_background_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'social.twittermessage': {
            'Meta': {'object_name': 'TwitterMessage', '_ormbases': [u'social.Message']},
            '_entities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'favorited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_reply_to_screen_name': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'in_reply_to_status_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'in_reply_to_user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'retweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'twitter_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.TwitterAccount']", 'null': 'True', 'blank': 'True'}),
            'twitter_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['social.TwitterSearch']", 'null': 'True', 'blank': 'True'})
        },
        u'social.twitterpublicaccount': {
            'Meta': {'object_name': 'TwitterPublicAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'social.twittersearch': {
            'Meta': {'object_name': 'TwitterSearch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'search_until': ('django.db.models.fields.IntegerField', [], {'default': '1403031384'})
        },
        u'social.twittersetting': {
            'Meta': {'object_name': 'TwitterSetting'},
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        }
    }

    complete_apps = ['social']