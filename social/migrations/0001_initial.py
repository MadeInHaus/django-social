# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import social.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fb_id', models.CharField(help_text=b'11936081183 </br> Get Via: http://graph.facebook.com/nakedjuice', max_length=300)),
                ('last_poll_time', models.IntegerField(default=social.models.current_time)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookPublicAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text=b'Facebook username http://www.facebook.com/[username]', max_length=255)),
                ('fb_id', models.CharField(help_text=b'if you do not know this leave blank and it will be looked up based on username', max_length=300, null=True, blank=True)),
                ('last_poll_time', models.IntegerField(default=social.models.current_time)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_term', models.CharField(help_text=b"don't prefix with #", max_length=160, blank=True)),
                ('last_poll_time', models.IntegerField(default=social.models.current_time)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.CharField(max_length=255)),
                ('app_secret', models.CharField(max_length=255)),
                ('interval', models.IntegerField(default=15)),
                ('auto_approve', models.BooleanField(default=True)),
                ('filter_text', models.BooleanField(default=False)),
                ('filter_link', models.BooleanField(default=False)),
                ('filter_photo', models.BooleanField(default=False)),
                ('filter_video', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_id', models.BigIntegerField()),
                ('username', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('profile_picture', models.URLField()),
                ('access_token', models.CharField(max_length=255)),
                ('scrap_profile', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramPublicAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('instagram_id', models.BigIntegerField(default=0, help_text=b'if not known, leave 0 and it will be looked up')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_term', models.CharField(help_text=b"don't prefix with #", max_length=160, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('redirect_uri', models.URLField()),
                ('interval', models.IntegerField(default=15)),
                ('auto_approve', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_type', models.CharField(max_length=100, choices=[(b'post', b'Post'), (b'reply', b'Reply')])),
                ('media_type', models.CharField(default=b'unknown', max_length=20, db_index=True, choices=[(b'text', b'Text'), (b'photo', b'Photo'), (b'video', b'Video'), (b'vine', b'Vine'), (b'link', b'Link'), (b'unknown', b'Unkown')])),
                ('network', models.CharField(db_index=True, max_length=100, choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'rss', b'Rich Site Summary'), (b'instagram', b'Instagram')])),
                ('message', models.TextField(max_length=1000)),
                ('date', models.DateTimeField(db_index=True)),
                ('message_id', models.CharField(max_length=400, null=True, blank=True)),
                ('deeplink', models.URLField(null=True, blank=True)),
                ('blob', models.TextField(max_length=10000)),
                ('avatar', models.CharField(max_length=300, null=True, blank=True)),
                ('status', models.IntegerField(db_index=True, choices=[(10, b'pending'), (11, b'approved'), (12, b'rejected'), (15, b'favorited'), (13, b'legal')])),
                ('user_id', models.CharField(max_length=300, null=True, blank=True)),
                ('user_name', models.CharField(max_length=300, null=True, blank=True)),
                ('reply_id', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.Message')),
                ('comments', models.TextField(max_length=10000)),
                ('images', models.TextField(max_length=10000)),
                ('instagram_search', models.ManyToManyField(to='social.InstagramSearch', null=True, blank=True)),
            ],
            options={
            },
            bases=('social.message',),
        ),
        migrations.CreateModel(
            name='FacebookMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.Message')),
                ('facebook_account', models.ForeignKey(blank=True, to='social.FacebookAccount', null=True)),
                ('facebook_public_account', models.ForeignKey(blank=True, to='social.FacebookPublicAccount', null=True)),
            ],
            options={
            },
            bases=('social.message',),
        ),
        migrations.CreateModel(
            name='RSSAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_name', models.CharField(max_length=300, blank=True)),
                ('feed_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RSSMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.Message')),
                ('title', models.CharField(max_length=500)),
                ('_links', models.TextField(max_length=1000, blank=True)),
                ('_images', models.TextField(max_length=1000, blank=True)),
                ('rss_account', models.ForeignKey(to='social.RSSAccount')),
            ],
            options={
            },
            bases=('social.message',),
        ),
        migrations.CreateModel(
            name='RSSSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.IntegerField(default=15)),
                ('auto_approve', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_id', models.BigIntegerField()),
                ('description', models.CharField(max_length=160, blank=True)),
                ('verified', models.BooleanField(default=False)),
                ('entities', models.TextField(blank=True)),
                ('profile_image_url_https', models.URLField(blank=True)),
                ('followers_count', models.IntegerField(default=0)),
                ('protected', models.BooleanField(default=False)),
                ('profile_background_image_url_https', models.URLField(blank=True)),
                ('profile_background_image_url', models.URLField(blank=True)),
                ('name', models.CharField(max_length=400, blank=True)),
                ('screen_name', models.CharField(max_length=400)),
                ('url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=400, blank=True)),
                ('oauth_token', models.CharField(max_length=255, blank=True)),
                ('oauth_secret', models.CharField(max_length=255, blank=True)),
                ('poll_count', models.IntegerField(default=0, editable=False)),
                ('parse_timeline_tweets', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.Message')),
                ('in_reply_to_status_id', models.BigIntegerField(null=True)),
                ('source', models.CharField(max_length=400)),
                ('retweeted', models.BooleanField(default=False)),
                ('_entities', models.TextField(null=True, blank=True)),
                ('in_reply_to_screen_name', models.CharField(max_length=400, null=True)),
                ('in_reply_to_user_id', models.BigIntegerField(null=True)),
                ('retweet_count', models.IntegerField(default=0)),
                ('favorited', models.BooleanField(default=False)),
                ('twitter_account', models.ForeignKey(blank=True, to='social.TwitterAccount', null=True)),
            ],
            options={
            },
            bases=('social.message',),
        ),
        migrations.CreateModel(
            name='TwitterPublicAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(help_text=b'Twitter account name', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_term', models.CharField(help_text=b'@dino or #dino', max_length=160, blank=True)),
                ('search_until', models.IntegerField(default=social.models.current_time)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consumer_key', models.CharField(max_length=255)),
                ('consumer_secret', models.CharField(max_length=255)),
                ('interval', models.IntegerField(default=15)),
                ('auto_approve', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='twittermessage',
            name='twitter_public_account',
            field=models.ForeignKey(blank=True, to='social.TwitterPublicAccount', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twittermessage',
            name='twitter_search',
            field=models.ManyToManyField(to='social.TwitterSearch', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='_tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(related_name='reply', blank=True, editable=False, to='social.Message', null=True),
            preserve_default=True,
        ),
    ]
