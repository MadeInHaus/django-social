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
    


class Twitter(Social):
    _entities = models.TextField(max_length=1000,null=True, blank=True)
    @property
    def entities(self):
        return json.loads(self.entities) if self.entities else {}
    def save(self, *args, **kwargs):
        self.network = 'twitter'
        super(Twitter, self).save(*args, **kwargs)
        

class Facebook(Social):
    def save(self, *args, **kwargs):
        self.network = 'facebook'
        super(Facebook, self).save(*args, **kwargs)