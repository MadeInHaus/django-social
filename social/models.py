from . import settings
import json
from django.db import models


MESSAGE_TYPE =  (
                    ('post', 'Post'),
                    ('reply', 'Reply'),
                )

NETWORK =       (
                    ('facebook', 'Facebook'),
                    ('twitter', 'Twitter'),
                )

STATUS_LIST =   (
                    (0, 'pending'),
                    (1, 'approved'),
                    (2, 'rejected'),
                )


class Message(models.Model):
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE)
    network = models.CharField(max_length=100, choices=NETWORK)
    message = models.TextField(max_length=1000)
    avatar = models.CharField(max_length=300,null=True,blank=True)
    status = models.IntegerField(choices=STATUS_LIST)
    def __unicode__(self):
        return str(self.pk)

class Social(Message):
    user_id = models.CharField(max_length=300)
    user_name = models.CharField(max_length=300)
    date = models.DateTimeField()
    message_id = models.CharField(max_length=200, null=True,blank=True)
    deeplink = models.URLField(null=True,blank=True)
    reply_to = models.ForeignKey('Social', related_name='reply',null=True,blank=True)
    reply_id = models.CharField(max_length=300,null=True,blank=True)



class TwitterMessage(Social):
    text = models.CharField(max_length=140)
    in_reply_to_status_id = models.BigIntegerField(null=True)
    tweet_id = models.BigIntegerField()
    source = models.CharField(max_length=100)
    retweeted = models.BooleanField(default=False)
    _entities = models.TextField(null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=100, null=True)
    in_reply_to_user_id = models.BigIntegerField(null=True)
    retweet_count = models.IntegerField()
    favorited = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    @property
    def entities(self):
        return json.loads(self._entities) if self._entities else {}

    @entities.setter
    def set_entities(self, entities):
        self._entities = json.dumps(entities)

    def save(self, *args, **kwargs):
        self.network = 'twitter'
        if not self.status:
            self.status = 1 if settings.SOCIAL_TWITTER_AUTO_APPROVE else 0
        super(TwitterMessage, self).save(*args, **kwargs)

class TwitterAccount(models.Model):
    user_id = models.BigIntegerField()
    description = models.CharField(max_length=160, blank=True)
    verified = models.BooleanField(default=False)
    entities = models.TextField()
    profile_image_url_https = models.URLField(blank=True)
    followers_count = models.IntegerField(default=0)
    protected = models.BooleanField(default=False)
    profile_background_image_url_https = models.URLField(blank=True)
    profile_background_image_url = models.URLField(blank=True)
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.screen_name


class FacebookMessage(Social):
    facebook_account = models.ForeignKey('FacebookAccount',null=True, blank=True)
    def save(self, *args, **kwargs):
        self.network = 'facebook'
        if not self.status:
            self.status = 1 if settings.SOCIAL_FACEBOOK_AUTO_APPROVE else 0
        super(FacebookMessage, self).save(*args, **kwargs)

    @staticmethod
    def from_json(json):
        fb = FacebookMessage()
        # TODO parse this data!!!!
        print('hi')
        return fb

    @classmethod
    def create_from_json(cls,json):
        instance = cls.from_json(json)
        # TODO once you're done, uncomment this
        #instance.save()
        return instance

class FacebookAccount(models.Model):
    fb_id = models.CharField(max_length=300,
        help_text='11936081183 </br> Get Via: http://graph.facebook.com/nakedjuice')
    def __unicode__(self):
        return self.fb_id
