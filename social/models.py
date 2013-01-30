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
    status = models.IntegerField(choices=STATUS_LIST, default=settings.SOCIAL_AUTO_APPROVE, null=True)
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
    _entities = models.TextField(max_length=1000,null=True, blank=True)
    @property
    def entities(self):
        return json.loads(self.entities) if self.entities else {}
    def save(self, *args, **kwargs):
        self.network = 'twitter'
        super(Twitter, self).save(*args, **kwargs)
        

class FacebookMessage(Social):
    facebook_account = models.ForeignKey('FacebookAccount',null=True, blank=True)
    def save(self, *args, **kwargs):
        self.network = 'facebook'
        super(FacebookMessage, self).save(*args, **kwargs)
    
    @staticmethod
    def from_json(json):
        fb = FacebookMessage()
        # TODO parse this data!!!!
        print(json)
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
