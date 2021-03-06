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
from social.utils.facebook import parse_facebook_video_embed, parse_facebook_picture_embed,\
    parse_facebook_normal_picture_url
from social.utils.twitter import parse_twitter_video_embed, parse_twitter_picture_embed,\
    twitter_msg_has_an_image
from social.utils.instagram import parse_instagram_video_embed,\
    parse_instagram_picture_embed

from urlparse import parse_qs, urlparse

from taggit.managers import TaggableManager
from .utils.editable_tags import editable_tags
from .services.facebook import get_id_from_username
from .services.instagram import InstagramPublicAPI
from utils.twitter import parse_twitter_picture

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
LEGAL = 13
FAVORITED = 15


STATUS_LIST =   (
                    (PENDING, 'pending'),
                    (APPROVED, 'approved'),
                    (REJECTED, 'rejected'),
                    (FAVORITED, 'favorited'),
                    (LEGAL, 'legal'),
                )

STATUS_NAME_LOOKUP = {l[0]: l[1] for l in STATUS_LIST}


def current_time():
    """returns the current time for use in default as a callable"""
    return int(time.time())

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
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE, default="unknown", db_index=True)
    network = models.CharField(max_length=100, choices=NETWORK, db_index=True)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(db_index=True)
    message_id = models.CharField(max_length=400, null=True,blank=True)
    deeplink = models.URLField(null=True,blank=True)
    blob = models.TextField(max_length=10000)
    avatar = models.CharField(max_length=300,null=True,blank=True)
    status = models.IntegerField(choices=STATUS_LIST,db_index=True)
    user_id = models.CharField(max_length=300, blank=True, null=True)
    user_name = models.CharField(max_length=300, blank=True, null=True)
    reply_to = models.ForeignKey('Message', related_name='reply',null=True,blank=True,editable=False)
    reply_id = models.CharField(max_length=300,null=True,blank=True)

    _tags = TaggableManager(blank=True)
    _tags.short_description = "Moderation Tags"
    _tags.verbose_name = "Moderation Tags"
    
    tags = editable_tags(_tags)
    tags.admin_order_field = '_tags'
    tags.short_description = "Moderation Tags"
    tags.verbose_name = "Moderation Tags"

    def save(self, *args, **kwargs):
        if hasattr(self, '_blob'):
            #remove cached blob on save
            delattr(self, '_blob')
        super(Message, self).save(*args, **kwargs)

    def get_blob(self):
        # caches the parsed blob for further use
        # note this assumes blobs are readonly
        if not hasattr(self, '_blob'):
            self._blob = json.loads(self.blob)

        return self._blob

    @property
    def image_link(self):
        blob = self.get_blob()
        if self.media_type == "video":
            link = blob.get('link')
            if link:
                params = parse_qs(urlparse(link).query)
                if 'youtube' in link:
                    return 'http://img.youtube.com/vi/{}/hqdefault.jpg'.format(params.get('v',['',])[0])

        if self.network == "facebook":
            pic_link = blob.get('picture')
            if pic_link and 'safe_image.php' in pic_link:
                pic_link = parse_qs(urlparse(pic_link).query).get('url', [None,])[0]
            if pic_link:
                pic_link = pic_link.replace('_s', '_b').replace('_t', '_b')
            return pic_link
            
        if self.network == "instagram":
            return blob.get('images', {}).get('standard_resolution', {}).get('url', '')

        if self.network == "twitter" and self.media_type == 'photo':
            return self.twittermessage.get_image_standard()

        return ''

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

    admin_media_preview.short_description = 'Media Preview'
    admin_media_preview.allow_tags = True


class TwitterMessage(Message):
    #text = models.CharField(max_length=140)
    in_reply_to_status_id = models.BigIntegerField(null=True,blank=True)
    #removing this, using message_id
    #tweet_id = models.BigIntegerField()
    source = models.CharField(max_length=400)
    retweeted = models.BooleanField(default=False)
    _entities = models.TextField(null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=400, null=True, blank=True)
    in_reply_to_user_id = models.BigIntegerField(null=True, blank=True)
    retweet_count = models.IntegerField(default=0)
    favorited = models.BooleanField(default=False)
    twitter_search = models.ManyToManyField('TwitterSearch',null=True,blank=True)
    twitter_account = models.ForeignKey('TwitterAccount',null=True,blank=True)
    twitter_public_account = models.ForeignKey('TwitterPublicAccount',null=True,blank=True)
    #created_at = models.DateTimeField()

    @property
    def entities(self):
        return json.loads(self._entities) if self._entities else {}

    @entities.setter
    def entities(self, entities):
        self._entities = json.dumps(entities, sort_keys=True, indent=4)

    def get_image_standard(self):
        return parse_twitter_picture(self.get_blob())

    def save(self, *args, **kwargs):
        self.network = 'twitter'
        if self.status is None:
            self.status = APPROVED if TwitterSetting.objects.get().auto_approve else PENDING
        super(TwitterMessage, self).save(*args, **kwargs)

    # create tweet and make sure it's unique based on id_str and search term
    @staticmethod
    def create_from_json(obj, search=None, account=None, media_type_filter=None):
        if type(account) == TwitterPublicAccount:
            public_account = account
            account = None
        else:
            public_account = None

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

        if twitter_msg_has_an_image(obj):
            message.media_type = 'photo'

        if media_type_filter and message.media_type not in media_type_filter:
            raise TweetFiltered

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
        message.blob = json.dumps(obj, sort_keys=True, indent=4)
        message.avatar = obj.get('user',{}).get('profile_image_url_https','')
        message.save()
        if search:
            message.twitter_search.add(search)
        if account:
            message.twitter_account = account
        if public_account:
            message.twitter_public_account = public_account
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


class TwitterPublicAccount(models.Model):
    screen_name = models.CharField(max_length=255, help_text="Twitter account name")
    parse_timeline_tweets = True # always parse public accounts

    def __unicode__(self):
        return self.screen_name


class TwitterSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='@dino or #dino')
    search_until = models.IntegerField(default=current_time)
    filter_for_images = models.BooleanField(default=False)
    account = models.CharField(default='', max_length=30, blank=True,
                               help_text="Account handle to search, leave blank to search all users")

    def __unicode__(self):
        return "{} @{}".format(self.search_term, self.account) if self.account else self.search_term


class FacebookMessage(Message):
    facebook_account = models.ForeignKey('FacebookAccount',null=True, blank=True)
    facebook_public_account = models.ForeignKey('FacebookPublicAccount',null=True, blank=True)

    def __unicode__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.network = 'facebook'
        if self.status is None:
            self.status = APPROVED if FacebookSetting.objects.get().auto_approve else PENDING
        super(FacebookMessage, self).save(*args, **kwargs)

    @staticmethod
    def create_from_json(json_obj, account=None, fbapi=None):
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

        if type(account) == FacebookPublicAccount:
            public_account = account
            account = None

        if message_type not in fb_setting.filter_list():
            fb_message.facebook_account = account
            fb_message.facebook_public_account = public_account
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
            if 'picture' in json_obj:
                if fbapi:
                    json_obj['picture_data'] = fbapi.get_photo_data(json_obj) or {}
                    json_obj['picture_normal'] = json_obj['picture_data']['source'] if 'source' in json_obj['picture_data'] else parse_facebook_normal_picture_url(json_obj)
                else:
                    json_obj['picture_data'] = {}
                    json_obj['picture_normal'] = parse_facebook_normal_picture_url(json_obj)

                # GOING TO ALWAYS SET STATUS PENDING WHEN WE GET AN ERROR ACCESSING THE PHOTO # TODO SOMETHING IS WRONG WITH THIS BUT WE DON'T KNOW WHAT
                if 'error' in json_obj['picture_data']:
                    fb_message.status = PENDING


            fb_message.blob = json.dumps(json_obj, sort_keys=True, indent=4)
            fb_message.media_type = message_type
            fb_message.save()
        return fb_message


class FacebookAccount(models.Model):
    fb_id = models.CharField(max_length=300,
        help_text='11936081183 </br> Get Via: http://graph.facebook.com/nakedjuice')
    last_poll_time = models.IntegerField(default=current_time)

    def get_id(self):
        if not self.fb_id:
            try:
                self.fb_id = get_id_from_username(self.username)
                self.save()
            except:
                return None
        return self.fb_id

    def __unicode__(self):
        return self.fb_id


class FacebookPublicAccount(models.Model):
    username = models.CharField(max_length=255, help_text="Facebook username http://www.facebook.com/[username]")
    fb_id = models.CharField(max_length=300, null=True, blank=True,
        help_text='if you do not know this leave blank and it will be looked up based on username')
    last_poll_time = models.IntegerField(default=current_time)

    def save(self, *args, **kwargs):
        print self.get_id()
        return models.Model.save(self, *args, **kwargs)

    def get_id(self):
        if not self.fb_id:
            try:
                self.fb_id = get_id_from_username(self.username)
                self.save()
            except:
                return None
        return self.fb_id

    def __unicode__(self):
        return self.username


class FacebookSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='don\'t prefix with #')
    last_poll_time = models.IntegerField(default=current_time)

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
        self._links = json.dumps(links, sort_keys=True, indent=4)

    @property
    def images(self):
        return json.loads(self._images) if self._images else []

    @images.setter
    def images(self, images):
        self._images = json.dumps(images, sort_keys=True, indent=4)


class InstagramSearch(models.Model):
    search_term = models.CharField(max_length=160, blank=True, help_text='don\'t prefix with #')
    username = models.CharField(max_length=255, null=True, blank=True,
                                help_text="If set, only this account will be searched")
    instagram_id = models.BigIntegerField(default=0,
                                          help_text="if not known, leave 0 and it will be looked up")
    last_id = models.CharField(max_length=42, null=True, blank=True,
                               help_text='greatest id seen so far for this search,  searches will search from this id forward')
    filter_for_images = models.BooleanField(default=False)
    filter_for_videos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.username and not self.instagram_id:
            instagram_setting = InstagramSetting.objects.get()
            instagram_api = InstagramPublicAPI(instagram_setting)
            self.instagram_id = instagram_api.get_id_from_username(self.username)
        return models.Model.save(self, *args, **kwargs)

    def get_filter(self):
        filter = []
        if self.filter_for_images:
            filter.append('photo')
        if self.filter_for_videos:
            filter.append('video')

        return None if filter == [] else filter

    def __unicode__(self):
        if self.username:
            return "{} @{}".format(self.search_term, self.username)
        return self.search_term


class InstagramAccount(models.Model):
    instagram_id = models.BigIntegerField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_picture = models.URLField()
    access_token = models.CharField(max_length=255)
    scrape_profile = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username

    def admin_image(self):
        return '<img src="{}">'.format(self.profile_picture)
    admin_image.allow_tags = True


class InstagramPublicAccount(models.Model):
    username = models.CharField(max_length=255)
    instagram_id = models.BigIntegerField(default=0,
                                          help_text="if not known, leave 0 and it will be looked up")

    def save(self, *args, **kwargs):
        if not self.instagram_id:
            instagram_setting = InstagramSetting.objects.get()
            instagram_api = InstagramPublicAPI(instagram_setting)
            self.instagram_id = instagram_api.get_id_from_username(self.username)
        return models.Model.save(self, *args, **kwargs)

    def __unicode__(self):
        return self.username

class InstagramMessage(Message):
    instagram_search = models.ManyToManyField('InstagramSearch', null=True, blank=True)
    comments = models.TextField(max_length=10000)
    images = models.TextField(max_length=10000)

    @staticmethod
    def create_from_json(media, search=None, filter_users=None, filter_media_type=None):
        if search and search.username:
            last_id = media.get('id', None)
            search.last_id = last_id if not search.last_id or search.last_id < last_id else search.last_id

        if filter_users and (media.get('user',{}).get('username') not in filter_users):
            raise IGUserFiltered('This user is not in the filter list.')
        if (filter_users and search 
            and (search.search_term not in media.get('caption',{}).get('text')
                 or search.search_term not in media.get('tags', []))):
            raise IGTermFiltered('This term not found in message')
            
        try:
            ig_media = InstagramMessage.objects.get(message_id=media.get('id'))
            if search:
                if ig_media.instagram_search.filter(pk=search.pk).exists():
                    raise IGMediaExistsError("Post already exists in DB: {}".format(ig_media.id))
                else:
                    ig_media.instagram_search.add(search)
            raise IGMediaExistsError("Post already exists in DB: {}".format(ig_media.id))
        except InstagramMessage.DoesNotExist:
            ig_media = InstagramMessage()
            ig_media.date = datetime.utcfromtimestamp(float(media.get('created_time', 0))).replace(tzinfo=utc)
            ig_media.comments = json.dumps(media.get('comments', {}).get('data', []), sort_keys=True, indent=4)
            ig_media.images = json.dumps(media.get('images', {}), sort_keys=True, indent=4)
            ig_media.message_id = media.get('id', '')
            ig_media.deeplink = media.get('link', '')
            ig_media.message_type = 'post'
            ig_media.media_type = media.get('type')
            if ig_media.media_type == 'image':
                ig_media.media_type = 'photo'
            if filter_media_type and ig_media.media_type not in filter_media_type:
                raise IGMediaFiltered('Media type not in filter list')
            if media.get('caption', {}):
                ig_media.message = media.get('caption', {}).get('text', '').encode('utf-8')
            ig_media.avatar = media.get('user', {}).get('profile_picture', '')
            ig_media.blob = json.dumps(media, sort_keys=True, indent=4)
            ig_media.user_id = media.get('user', {}).get('id', '0')
            ig_media.user_name = media.get('user', {}).get('username', '')
            ig_media.save()
            if search:
                ig_media.instagram_search.add(search)
                ig_media.save()

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

class TweetFiltered(Exception):
    pass

class IGMediaExistsError(Exception):
    pass

class IGMediaFiltered(Exception):
    pass

class IGUserFiltered(Exception):
    pass

class IGTermFiltered(Exception):
    pass



@receiver(post_save, sender=TwitterAccount)
def reset_poll_count(sender, instance, created, raw, **kwargs):
    if created:
        accounts = sender.objects.all().update(poll_count=0)
