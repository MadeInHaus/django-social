# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
	forward_map = {
		0: 10,
		1: 11,
		2: 12,
		5: 15,
		}
	default = 10	

	for obj in orm['social.TwitterMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.FacebookMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.RSSMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.InstagramMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()


    def backwards(self, orm):
	forward_map = {
		10: 0,
		11: 1,
		12: 2,
		15: 5,
		}
	default = 0	

	for obj in orm['social.TwitterMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.FacebookMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.RSSMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()

	for obj in orm['social.InstagramMessage'].objects.all():
		obj.status = forward_map.get(obj.status, default)
		obj.save()



    models = {
        u'social.facebookaccount': {
            'Meta': {'object_name': 'FacebookAccount'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poll_time': ('django.db.models.fields.IntegerField', [], {'default': '1375388862'})
        },
        u'social.facebookmessage': {
            'Meta': {'object_name': 'FacebookMessage', '_ormbases': [u'social.Message']},
            'facebook_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.FacebookAccount']", 'null': 'True', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'social.facebooksetting': {
            'Meta': {'object_name': 'FacebookSetting'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        },
        u'social.instagrammessage': {
            'Meta': {'object_name': 'InstagramMessage', '_ormbases': [u'social.Message']},
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'images': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'instagram_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['social.InstagramSearch']", 'null': 'True', 'blank': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
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
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        },
        u'social.message': {
            'Meta': {'object_name': 'Message'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blob': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deeplink': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reply_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reply'", 'null': 'True', 'to': u"orm['social.Message']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
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
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parse_timeline_tweets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poll_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile_background_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_background_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'twitter_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'social.twittermessage': {
            'Meta': {'object_name': 'TwitterMessage', '_ormbases': [u'social.Message']},
            '_entities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'favorited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_reply_to_screen_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'in_reply_to_status_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'in_reply_to_user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'retweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'twitter_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social.TwitterAccount']", 'null': 'True', 'blank': 'True'}),
            'twitter_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['social.TwitterSearch']", 'null': 'True', 'blank': 'True'})
        },
        u'social.twittersearch': {
            'Meta': {'object_name': 'TwitterSearch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'search_until': ('django.db.models.fields.IntegerField', [], {'default': '1375388862'})
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
    symmetrical = True
