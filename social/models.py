from . import settings
import json
import time
import logging
from time import mktime
from datetime import datetime
from django.db import models
from django.utils.timezone import utc
from django.db.models.signals import post_save
from django.dispatch import receiver

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

MESSAGE_TYPE =  (
                    ('post', 'Post'),
                    ('reply', 'Reply'),
                )

NETWORK =       (
                    ('facebook', 'Facebook'),
                    ('twitter', 'Twitter'),
                    ('rss', 'Rich Site Summary'),
                    ('instagram', 'Instagram'),
                )

STATUS_LIST =   (
                    (0, 'pending'),
                    (1, 'approved'),
                    (2, 'rejected'),
                    (5, 'favorited'),
                )


class Message(models.Model):
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE)
    network = models.CharField(max_length=100, choices=NETWORK)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField()
    message_id = models.CharField(max_length=200, null=True,blank=True)
    deeplink = models.URLField(null=True,blank=True)
    blob = models.TextField(max_length=10000)
    avatar = models.CharField(max_length=300,null=True,blank=True)
    status = models.IntegerField(choices=STATUS_LIST)
    user_id = models.CharField(max_length=300, blank=True)
    user_name = models.CharField(max_length=300, blank=True)
    reply_to = models.ForeignKey('Message', related_name='reply',null=True,blank=True)
    reply_id = models.CharField(max_length=300,null=True,blank=True)
    
    def __unicode__(self):
        return str(self.pk)


class TwitterMessage(Message):
    #text = models.CharField(max_length=140)
    in_reply_to_status_id = models.BigIntegerField(null=True)
    #removing this, using message_id
    #tweet_id = models.BigIntegerField()
    source = models.CharField(max_length=200)
    retweeted = models.BooleanField(default=False)
    _entities = models.TextField(null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=200, null=True)
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
        if not self.status:
            self.status = 1 if settings.SOCIAL_TWITTER_AUTO_APPROVE else 0
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
            log.debug('[twitter create debug] duplicate ids attempted to be added')
            raise TweetExistsError
            return

        message = TwitterMessage()
        message.in_reply_to_status_id = obj.get('in_reply_to_status_id',0)
        message.source = obj.get('source','')
        message.retweeted = obj.get('retweeted','False')
        message._entities = obj.get('entities','')
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
    name = models.CharField(max_length=200,blank=True)
    screen_name = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200,blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)
    poll_count = models.IntegerField(default=0,editable=False)
    parse_timeline_tweets = models.BooleanField(default=settings.SOCIAL_TWITTER_FOLLOW_ACCOUNTS)

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
        account.statuses_count          = obj['statuses_count']
        account.oauth_token             = oauth_token
        account.oauth_secret            = oauth_token_secret
        account.save()

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
        if not self.status:
            self.status = 1 if settings.SOCIAL_FACEBOOK_AUTO_APPROVE else 0
        super(FacebookMessage, self).save(*args, **kwargs)


    @staticmethod
    def create_from_json(account,json):
        fb_message = FacebookMessage()
        
        # already created, need to update?
        saved_message = FacebookMessage.objects.filter(message_id=json['id'])
        if saved_message:
            #raise Exception("Post already exists in DB")
            return saved_message[0]


        # create a status 
        if json.get('type', False) == 'status' :
            fb_message.facebook_account = account
            fb_message.message_type = 'post'
            fb_message.message = json.get('message','')
            # NEED TO DECIDE IF THIS IS BEST LOGIC!
            if fb_message.message == '': return
            fb_message.avatar = 'https://graph.facebook.com/{0}/picture'.format(json['from']['id'])
            fb_message.user_id = json['from']['id']
            fb_message.user_name = json['from']['name']
            time_struct = time.strptime(json['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
            fb_message.date = datetime.utcfromtimestamp(mktime(time_struct)).replace(tzinfo=utc)
            fb_message.message_id = json['id']
            temparr = json['id'].split('_')
            fb_message.deeplink = 'https://www.facebook.com/{0}/posts/{1}'.format(temparr[0],temparr[1])
            fb_message.blob = json
            fb_message.save()
        return fb_message
        

class FacebookAccount(models.Model):
    fb_id = models.CharField(max_length=300,
        help_text='11936081183 </br> Get Via: http://graph.facebook.com/nakedjuice')
    last_poll_time = models.IntegerField(default=int(time.time()))
    def __unicode__(self):
        return self.fb_id

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

    def save(self, *args, **kwargs):
        self.network = 'rss'
        if not self.status:
            self.status = 1 if settings.SOCIAL_RSS_AUTO_APPROVE else 0
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
    search_term = models.CharField(max_length=160, blank=True, help_text='dont prefix with #')
    def __unicode__(self):
        return self.search_term

class InstagramMessage(Message):
    instagram_search = models.ManyToManyField('InstagramSearch',null=True,blank=True)
    comments = models.TextField(max_length=10000)
    images = models.TextField(max_length=10000)


    @staticmethod
    def create_from_json(media,search=None):
        saved_message = InstagramMessage.objects.filter(message_id=media.get('id','none'))
        if saved_message:
            tmp_message = saved_message.filter(instagram_search__search_term=search.search_term)
            if tmp_message:
                raise IGMediaExistsError("Post already exists in DB")
                return saved_message[0]
            saved_message = saved_message[0]
            saved_message.instagram_search.add(search)
            saved_message.save()
            return
        ig_media = InstagramMessage()
        ig_media.date = datetime.utcfromtimestamp(float(media.get('created_time',0))).replace(tzinfo=utc)
        ig_media.comments = json.dumps(media.get('comments',{}).get('data',[]))
        ig_media.images = json.dumps(media.get('images',{}))
        ig_media.message_id = media.get('id','')
        ig_media.deeplink = media.get('link','')
        ig_media.message_type = 'post'
        ig_media.message = json.dumps(media.get('caption',{}).get('text',''))
        ig_media.avatar = media.get('user',{}).get('profile_picture','')
        ig_media.blob = json.dumps(media)
        ig_media.user_id = media.get('user',{}).get('id','0')
        ig_media.user_name = media.get('user',{}).get('username','')
        ig_media.save()
        if search:
            ig_media.instagram_search.add(search)
            ig_media.save()
        return ig_media

    
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
        if not self.status:
            self.status = 1 if settings.SOCIAL_INSTAGRAM_AUTO_APPROVE else 0
        super(InstagramMessage, self).save(*args, **kwargs)

class TweetExistsError(Exception):
    pass

class IGMediaExistsError(Exception):
    pass

@receiver(post_save, sender=TwitterAccount)
def search_nearby_schools(sender, instance, created, raw, **kwargs):
    if created == True:
        accounts = sender.objects.all().update(poll_count=0)
