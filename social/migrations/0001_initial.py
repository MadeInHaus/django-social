# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('social_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('deeplink', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('blob', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('avatar', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reply', null=True, to=orm['social.Message'])),
            ('reply_id', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('social', ['Message'])

        # Adding model 'TwitterMessage'
        db.create_table('social_twittermessage', (
            ('message_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.Message'], unique=True, primary_key=True)),
            ('in_reply_to_status_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('retweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_entities', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('in_reply_to_screen_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('in_reply_to_user_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('retweet_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('favorited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.TwitterAccount'], null=True, blank=True)),
        ))
        db.send_create_signal('social', ['TwitterMessage'])

        # Adding M2M table for field twitter_search on 'TwitterMessage'
        db.create_table('social_twittermessage_twitter_search', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('twittermessage', models.ForeignKey(orm['social.twittermessage'], null=False)),
            ('twittersearch', models.ForeignKey(orm['social.twittersearch'], null=False))
        ))
        db.create_unique('social_twittermessage_twitter_search', ['twittermessage_id', 'twittersearch_id'])

        # Adding model 'TwitterAccount'
        db.create_table('social_twitteraccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entities', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('profile_image_url_https', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('followers_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_background_image_url_https', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('profile_background_image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('oauth_secret', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('poll_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parse_timeline_tweets', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('social', ['TwitterAccount'])

        # Adding model 'TwitterSearch'
        db.create_table('social_twittersearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('search_until', self.gf('django.db.models.fields.IntegerField')(default=1368215245)),
        ))
        db.send_create_signal('social', ['TwitterSearch'])

        # Adding model 'FacebookMessage'
        db.create_table('social_facebookmessage', (
            ('message_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.Message'], unique=True, primary_key=True)),
            ('facebook_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.FacebookAccount'], null=True, blank=True)),
        ))
        db.send_create_signal('social', ['FacebookMessage'])

        # Adding model 'FacebookAccount'
        db.create_table('social_facebookaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_poll_time', self.gf('django.db.models.fields.IntegerField')(default=1368215245)),
        ))
        db.send_create_signal('social', ['FacebookAccount'])

        # Adding model 'RSSAccount'
        db.create_table('social_rssaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('social', ['RSSAccount'])

        # Adding model 'RSSMessage'
        db.create_table('social_rssmessage', (
            ('message_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.Message'], unique=True, primary_key=True)),
            ('rss_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.RSSAccount'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('_links', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('_images', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('social', ['RSSMessage'])

        # Adding model 'InstagramSearch'
        db.create_table('social_instagramsearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal('social', ['InstagramSearch'])

        # Adding model 'InstagramMessage'
        db.create_table('social_instagrammessage', (
            ('message_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.Message'], unique=True, primary_key=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('images', self.gf('django.db.models.fields.TextField')(max_length=10000)),
        ))
        db.send_create_signal('social', ['InstagramMessage'])

        # Adding M2M table for field instagram_search on 'InstagramMessage'
        db.create_table('social_instagrammessage_instagram_search', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instagrammessage', models.ForeignKey(orm['social.instagrammessage'], null=False)),
            ('instagramsearch', models.ForeignKey(orm['social.instagramsearch'], null=False))
        ))
        db.create_unique('social_instagrammessage_instagram_search', ['instagrammessage_id', 'instagramsearch_id'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('social_message')

        # Deleting model 'TwitterMessage'
        db.delete_table('social_twittermessage')

        # Removing M2M table for field twitter_search on 'TwitterMessage'
        db.delete_table('social_twittermessage_twitter_search')

        # Deleting model 'TwitterAccount'
        db.delete_table('social_twitteraccount')

        # Deleting model 'TwitterSearch'
        db.delete_table('social_twittersearch')

        # Deleting model 'FacebookMessage'
        db.delete_table('social_facebookmessage')

        # Deleting model 'FacebookAccount'
        db.delete_table('social_facebookaccount')

        # Deleting model 'RSSAccount'
        db.delete_table('social_rssaccount')

        # Deleting model 'RSSMessage'
        db.delete_table('social_rssmessage')

        # Deleting model 'InstagramSearch'
        db.delete_table('social_instagramsearch')

        # Deleting model 'InstagramMessage'
        db.delete_table('social_instagrammessage')

        # Removing M2M table for field instagram_search on 'InstagramMessage'
        db.delete_table('social_instagrammessage_instagram_search')


    models = {
        'social.facebookaccount': {
            'Meta': {'object_name': 'FacebookAccount'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_poll_time': ('django.db.models.fields.IntegerField', [], {'default': '1368215245'})
        },
        'social.facebookmessage': {
            'Meta': {'object_name': 'FacebookMessage', '_ormbases': ['social.Message']},
            'facebook_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.FacebookAccount']", 'null': 'True', 'blank': 'True'}),
            'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        'social.instagrammessage': {
            'Meta': {'object_name': 'InstagramMessage', '_ormbases': ['social.Message']},
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'images': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'instagram_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.InstagramSearch']", 'null': 'True', 'blank': 'True'}),
            'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social.Message']", 'unique': 'True', 'primary_key': 'True'})
        },
        'social.instagramsearch': {
            'Meta': {'object_name': 'InstagramSearch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'})
        },
        'social.message': {
            'Meta': {'object_name': 'Message'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blob': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deeplink': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reply_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reply'", 'null': 'True', 'to': "orm['social.Message']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'social.rssaccount': {
            'Meta': {'object_name': 'RSSAccount'},
            'feed_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social.rssmessage': {
            'Meta': {'object_name': 'RSSMessage', '_ormbases': ['social.Message']},
            '_images': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            '_links': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'rss_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.RSSAccount']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'social.twitteraccount': {
            'Meta': {'object_name': 'TwitterAccount'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'entities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'social.twittermessage': {
            'Meta': {'object_name': 'TwitterMessage', '_ormbases': ['social.Message']},
            '_entities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'favorited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_reply_to_screen_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'in_reply_to_status_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'in_reply_to_user_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'retweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'twitter_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.TwitterAccount']", 'null': 'True', 'blank': 'True'}),
            'twitter_search': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.TwitterSearch']", 'null': 'True', 'blank': 'True'})
        },
        'social.twittersearch': {
            'Meta': {'object_name': 'TwitterSearch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'search_until': ('django.db.models.fields.IntegerField', [], {'default': '1368215245'})
        }
    }

    complete_apps = ['social']