import json
import time
import logging
from time import mktime
from datetime import datetime
from django.db import models
from django.utils.timezone import utc
from django.db.models.signals import post_save
from django.dispatch import receiver
from urlparse import urlparse, parse_qsl, parse_qs
from social.utils.facebook import parse_facebook_video_embed, parse_facebook_picture_embed
from social.utils.twitter import parse_twitter_video_embed, parse_twitter_picture_embed
from social.utils.instagram import parse_instagram_video_embed,\
    parse_instagram_picture_embed

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

MESSAGE_TYPE =  (
                    ('post', 'Post'),
                    ('reply', 'Reply'),

                )

MEDIA_TYPE =  (
                    ('text', 'Text'),
                    ('photo', 'Photo'),
                    ('video', 'Video'),
                    ('vine', 'Vine'),
                    ('link', 'Link'),
                    ('unknown', 'Unkown'),
                )

NETWORK =       (
                    ('facebook', 'Facebook'),
                    ('twitter', 'Twitter'),
                    ('rss', 'Rich Site Summary'),
                    ('instagram', 'Instagram'),
                )

PENDING = 10
APPROVED = 11
REJECTED = 12
FAVORITED = 15

STATUS_LIST =   (
                    (PENDING, 'pending'),
                    (APPROVED, 'approved'),
                    (REJECTED, 'rejected'),
                    (FAVORITED, 'favorited'),
                )


class TwitterSetting(models.Model):
    consumer_key = models.CharField(max_length=255, blank=False)
    consumer_secret = models.CharField(max_length=255, blank=False)
    interval = models.IntegerField(blank=False, default=15)
    auto_approve = models.BooleanField(default=True)

    def __unicode__(self):
        return self.consumer_key

class FacebookSetting(models.Model):
    app_id = models.CharField(max_length=255, blank=False)
    app_secret = models.CharField(max_length=255, blank=False)
    interval = models.IntegerField(blank=False, default=15)
    auto_approve = models.BooleanField(default=True)
    filter_text =  models.BooleanField(default=False)
    filter_link =  models.BooleanField(default=False)
    filter_photo =  models.BooleanField(default=False)
    filter_video =  models.BooleanField(default=False)

    def __unicode__(self):
        return self.app_id

    def filter_list(self):
        types = ['text', 'link', 'photo', 'video']
        return [t for t in types if getattr(self, 'filter_{}'.format(t))]

class InstagramSetting(models.Model):
    client_id = models.CharField(max_length=255, blank=False)
    client_secret = models.CharField(max_length=255, blank=False)
    redirect_uri = models.URLField()
    interval = models.IntegerField(blank=False, default=15)
    auto_approve = models.BooleanField(default=True)

    def __unicode__(self):
        return self.client_id

class RSSSetting(models.Model):
    interval = models.IntegerField(blank=False, default=15)
    auto_approve = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Interval {}s'.format(self.interval)

class Message(models.Model):
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE, default="unknown")
    network = models.CharField(max_length=100, choices=NETWORK)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField()
    message_id = models.CharField(max_length=400, null=True,blank=True)
    deeplink = models.URLField(null=True,blank=True)
    blob = models.TextField(max_length=10000)
    avatar = models.CharField(max_length=300,null=True,blank=True)
    status = models.IntegerField(choices=STATUS_LIST)
    user_id = models.CharField(max_length=300, blank=True, null=True)
    user_name = models.CharField(max_length=300, blank=True, null=True)
    reply_to = models.ForeignKey('Message', related_name='reply',null=True,blank=True)
    reply_id = models.CharField(max_length=300,null=True,blank=True)

    def get_blob(self):
        return json.loads(self.blob)

    def __unicode__(self):
        return '-'.join([self.network, str(self.pk)])


    def admin_facebook_media_preview(self):
        msg = self.get_blob()
        
        if self.media_type == "video":
            return parse_facebook_video_embed(msg)
        elif self.media_type == "photo":
            return parse_facebook_picture_embed(msg)

        return ''


    def admin_twitter_media_preview(self):
        msg = self.get_blob()
        
        if self.media_type in ["video", "vine"]:
            return parse_twitter_video_embed(msg)
        elif self.media_type == "photo":
            return parse_twitter_picture_embed(msg)
        
        return ''


    def admin_instagram_media_preview(self):
        msg = self.get_blob()
        
        if self.media_type == "video":
            return parse_instagram_video_embed(msg)
        elif self.media_type == "photo":
            return parse_instagram_picture_embed(msg)
        
        return ''

    def admin_rss_media_preview(self):
        return ''

    def admin_media_preview(self):
        admin_media_preview_func = "admin_{}_media_preview".format(self.network)
        if not hasattr(self, admin_media_preview_func):
            return "unknown media type"
        
        return getattr(self, admin_media_preview_func)()
        
        print self.blob
        if self.blob:
            return u'<img height=200 width=200 src="%s" />' % json.loads(self.blob).get('low_resolution', {}).get('url', '')
    admin_media_preview.short_description = 'Media Preview'
    admin_media_preview.allow_tags = True


class TwitterMessage(Message):
    #text = models.CharField(max_length=140)
    in_reply_to_status_id = models.BigIntegerField(null=True)
    #removing this, using message_id
    #tweet_id = models.BigIntegerField()
    source = models.CharField(max_length=400)
    retweeted = models.BooleanField(default=False)
    _entities = models.TextField(null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=400, null=True)
    in_reply_to_user_id = models.BigIntegerField(null=True)
    retweet_count = models.IntegerField(default=0)
    favorited = models.BooleanField(default=False)
    twitter_search = models.ManyToManyField('TwitterSearch',null=True,blank=True)
    twitter_account = models.ForeignKey('TwitterAccount',null=True,blank=True)
    #created_at = models.DateTimeField()

    @property
    def entities(self):
        return json.loads(self._entities) if self._entities else {}

    @entities.setter
    def entities(self, entities):
        self._entities = json.dumps(entities)

    def save(self, *args, **kwargs):
        self.network = 'twitter'
        if self.status is None:
            self.status = APPROVED if TwitterSetting.objects.get().auto_approve else PENDING
        super(TwitterMessage, self).save(*args, **kwargs)

    # create tweet and make sure it's unique based on id_str and search term
    @staticmethod
    def create_from_json(obj,search=None,account=None):
        saved_message = TwitterMessage.objects.filter(message_id=obj.get('id_str',0))
        if saved_message and search:
            tmp_message = saved_message.filter(twitter_search__search_term=search.search_term)
            if tmp_message:
                # already exists, dont' add it, and throw error
                raise TweetExistsError
                return
            saved_message = saved_message[0]
            saved_message.twitter_search.add(search)
            saved_message.save()
            return saved_message
        elif saved_message:

            mid = str(saved_message[0].message_id)
            log.debug('[twitter create debug] duplicate ids attempted to be added: {}'.format(mid))
            raise TweetExistsError
            return

        message = TwitterMessage()
        message.in_reply_to_status_id = obj.get('in_reply_to_status_id',0)
        message.source = obj.get('source','')
        message.retweeted = obj.get('retweeted','False')
        message._entities = obj.get('entities','')
        meta = obj.get('entities',{});
        urls = meta.get('urls',[]);

        for url in urls:
            if url.get('expanded_url',None) == None:
                u = url.get('url','')
            else:
                u = url.get('expanded_url','')

            if 'youtu.be' in u or 'youtube.com' in u:
                message.media_type = 'video'

            if 'vine.co' in u:
                message.media_type = 'vine'

            if 'pic.twitter.com' in u:
                message.media_type = 'photo'

        message.in_reply_to_screen_name = obj.get('in_reply_to_screen_name','')
        message.in_reply_to_user_id = obj.get('in_reply_to_user_id','')
        message.retweet_count = obj.get('retweet_count',0)
        message.favorited = obj.get('favorited',False)
        message.user_id = obj.get('id_str')
        message.user_name = obj.get('user').get('screen_name')
        if obj.get('in_reply_to_screen_name',None) == None:
            message.message_type = 'post'
        else:
            message.message_type = 'reply'
        message.message = obj.get('text','')
        time_struct = time.strptime(obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        message.date = datetime.utcfromtimestamp(mktime(time_struct)).replace(tzinfo=utc)
        message.message_id = obj.get('id_str',0)
        message.deeplink = 'https://twitter.com/{0}/status/{1}'.format(message.user_name, message.message_id)
        message.blob = json.dumps(obj)
        message.avatar = obj.get('user',{}).get('profile_image_url_https','')
        message.save()
        if search:
            message.twitter_search.add(search)
        if account:
            message.twitter_account = account
        message.save()
        return message


class TwitterAccount(models.Model):
    twitter_id = models.BigIntegerField()
    description = models.CharField(max_length=160, blank=True)
    verified = models.BooleanField(default=False)
    entities = models.TextField(blank=True)
    profile_image_url_https = models.URLField(blank=True)
    followers_count = models.IntegerField(default=0)
    protected = models.BooleanField(default=False)
    profile_background_image_url_https = models.URLField(blank=True)
    profile_background_image_url = models.URLField(blank=True)
    name = models.CharField(max_length=400,blank=True)
    screen_name = models.CharField(max_length=400)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=400,blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)
    poll_count = models.IntegerField(default=0,editable=False)
    parse_timeline_tweets = models.BooleanField(default=False)

    def __unicode__(self):
        return self.screen_name

    @property
    def valid(self):
        try:
            return self._valid
        except AttributeError:
            self._valid = True
            return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value

    def update_credentials(self,authorized_tokens):
        self.oauth_token = authorized_tokens['oauth_token']
        self.oauth_secret = authorized_tokens['oauth_token_secret']
        self.save()

    @staticmethod
    def create_from_obj(obj, oauth_token, oauth_token_secret):
        account = TwitterAccount()
        account.twitter_id              = obj['id']
        account.screen_name             = obj['screen_name']
        account.profile_image_url_https = obj['profile_image_url_https']
        account.verified                = obj['verified']
        account.oauth_token             = oauth_token
        account.oauth_secret            = oauth_token_secret
        account.save()
        return account

class TwitterSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='@dino or #dino')
    search_until = models.IntegerField(default=int(time.time()))

    def __unicode__(self):
        return self.search_term

class FacebookMessage(Message):
    facebook_account = models.ForeignKey('FacebookAccount',null=True, blank=True)

    def __unicode__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.network = 'facebook'
        if self.status is None:
            self.status = APPROVED if FacebookSetting.objects.get().auto_approve else PENDING
        super(FacebookMessage, self).save(*args, **kwargs)

    @staticmethod
    def create_from_json(json_obj, account=None):
        fb_message = FacebookMessage()
        try:
            fb_setting = FacebookSetting.objects.all()[0]
        except:
            fb_setting = FacebookSetting()
            fb_setting.save()

        # already created, need to update?
        saved_message = FacebookMessage.objects.filter(message_id=json_obj['id'])
        if saved_message:
            #raise Exception("Post already exists in DB")
            return saved_message[0]

        if 'type' in json_obj and json_obj['type'] != 'status':
            message_type = json_obj['type']
        else:
            message_type = "text"

        if message_type not in fb_setting.filter_list():
            fb_message.facebook_account = account
            fb_message.message_type = 'post'
            fb_message.message = json_obj.get('message','')
            fb_message.avatar = 'https://graph.facebook.com/{0}/picture'.format(json_obj['from']['id'])
            fb_message.user_id = json_obj['from']['id']
            fb_message.user_name = json_obj['from']['name']
            time_struct = time.strptime(json_obj['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
            fb_message.date = datetime.utcfromtimestamp(mktime(time_struct)).replace(tzinfo=utc)
            fb_message.message_id = json_obj['id']
            temparr = json_obj['id'].split('_')
            fb_message.deeplink = 'https://www.facebook.com/{0}/posts/{1}'.format(temparr[0],temparr[1])
            fb_message.blob = json.dumps(json_obj)
            fb_message.media_type = message_type
            fb_message.save()
        return fb_message




class FacebookAccount(models.Model):
    fb_id = models.CharField(max_length=300,
        help_text='11936081183 </br> Get Via: http://graph.facebook.com/nakedjuice')
    last_poll_time = models.IntegerField(default=int(time.time()))
    def __unicode__(self):
        return self.fb_id

class FacebookSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='don\'t prefix with #')
    last_poll_time = models.IntegerField(default=int(time.time()))

    def __unicode__(self):
        return self.search_term


class RSSAccount(models.Model):
    feed_name = models.CharField(max_length=300, blank=True)
    feed_url = models.URLField()

    def __unicode__(self):
        return self.feed_name if self.feed_name else self.feed_url

class RSSMessage(Message):
    rss_account = models.ForeignKey('RSSAccount')
    title = models.CharField(max_length=500)
    _links = models.TextField(max_length=1000, blank=True)
    _images = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.network = 'rss'
        if self.status is None:
            self.status = APPROVED if RSSSetting.objects.get().auto_approve else PENDING

        super(RSSMessage, self).save(*args, **kwargs)

    @property
    def links(self):
        return json.loads(self._links) if self._links else []

    @links.setter
    def links(self, links):
        self._links = json.dumps(links)

    @property
    def images(self):
        return json.loads(self._images) if self._images else []

    @images.setter
    def images(self, images):
        self._images = json.dumps(images)

class InstagramSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='don\'t prefix with #')

    def __unicode__(self):
        return self.search_term

class InstagramAccount(models.Model):
    instagram_id = models.BigIntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_picture = models.URLField()
    access_token = models.CharField(max_length=255)
    scrap_profile = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username

    def admin_image(self):
        return '<img src="{}">'.format(self.profile_picture)
    admin_image.allow_tags = True

class InstagramMessage(Message):
    instagram_search = models.ManyToManyField('InstagramSearch', null=True, blank=True)
    comments = models.TextField(max_length=10000)
    images = models.TextField(max_length=10000)

    @staticmethod
    def create_from_json(media, search=None):
        try:
            ig_media = InstagramMessage.objects.get(message_id=media.get('id'))
            if search:
                if ig_media.instagram_search.filter(pk=search.pk).exists():
                    raise IGMediaExistsError("Post already exists in DB: {}".format(ig_media.id))
                else:
                    ig_media.instagram_search.add(search)
        except InstagramMessage.DoesNotExist:
            ig_media = InstagramMessage()
            ig_media.date = datetime.utcfromtimestamp(float(media.get('created_time', 0))).replace(tzinfo=utc)
            ig_media.comments = json.dumps(media.get('comments', {}).get('data', []))
            ig_media.images = json.dumps(media.get('images', {}))
            ig_media.message_id = media.get('id', '')
            ig_media.deeplink = media.get('link', '')
            ig_media.message_type = 'post'
            ig_media.media_type = media.get('type')
            if ig_media.media_type == 'image':
                ig_media.media_type = 'photo'
            if media.get('caption', {}):
                ig_media.message = media.get('caption', {}).get('text', '').encode('utf-8')
            ig_media.avatar = media.get('user', {}).get('profile_picture', '')
            ig_media.blob = json.dumps(media)
            ig_media.user_id = media.get('user', {}).get('id', '0')
            ig_media.user_name = media.get('user', {}).get('username', '')
            ig_media.save()
            if search:
                ig_media.instagram_search.add(search)

        return ig_media

    @property
    def get_images(self):
        return json.loads(self.images)

    @property
    def get_comments(self):
        return json.loads(self.comments)

    def get_image_low(self):
        return json.loads(self.images).get('low_resolution').get('url')

    def admin_image_low(self):
        return u'<img height=200 width=200 src="%s" />' % json.loads(self.images).get('low_resolution').get('url')
    admin_image_low.short_description = 'Image'
    admin_image_low.allow_tags = True

    def get_image_thumb(self):
        return json.loads(self.images).get('thumbnail').get('url')

    def get_image_standard(self):
        return json.loads(self.images).get('standard_resolution').get('url')

    def save(self, *args, **kwargs):
        self.network = 'instagram'
        if self.status is None:
            self.status = APPROVED if InstagramSetting.objects.get().auto_approve else PENDING

        super(InstagramMessage, self).save(*args, **kwargs)

class TweetExistsError(Exception):
    pass

class IGMediaExistsError(Exception):
    pass

@receiver(post_save, sender=TwitterAccount)
def reset_poll_count(sender, instance, created, raw, **kwargs):
    if created:
        accounts = sender.objects.all().update(poll_count=0)
