from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie import fields
from social.models import Message, TwitterMessage, FacebookMessage, RSSMessage, InstagramMessage

class MessageResource(ModelResource):
    blob = fields.DictField('get_blob',default=None)
    class Meta:
        include_resource_uri = False
        queryset = Message.objects.all()
        resource_name = 'message'
        serializer = Serializer(["json", "jsonp"])
        ordering = ['date',]

class TwitterResource(MessageResource):
    class Meta:
        queryset = TwitterMessage.objects.all()
        resource_name = 'twitter'

class FacebookResource(MessageResource):
    class Meta:
        queryset = FacebookMessage.objects.all()
        resource_name = 'facebook'

class RSSResource(MessageResource):
    class Meta:
        queryset = RSSMessage.objects.all()
        resource_name = 'rss'

class InstagramResource(MessageResource):
    images = fields.DictField('get_images',default=None)
    class Meta:
        queryset = InstagramMessage.objects.all()
        resource_name = 'instagram'
