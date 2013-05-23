from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie import fields
from social.models import Message, TwitterMessage, FacebookMessage, RSSMessage, InstagramMessage

class MessageResource(ModelResource):
    class Meta:
        include_resource_uri = False
        queryset = Message.objects.all()
        resource_name = 'message'
        serializer = Serializer(["json"])
        ordering = ['date',]
        


class TwitterResource(ModelResource):
    
    class Meta:
        include_resource_uri = False
        queryset = TwitterMessage.objects.all()
        resource_name = 'twitter'
        serializer = Serializer(["json"])
        ordering = ['date',]

class FacebookResource(ModelResource):
    
    class Meta:
        include_resource_uri = False
        queryset = FacebookMessage.objects.all()
        resource_name = 'facebook'
        serializer = Serializer(["json"])
        ordering = ['date',]

class RSSResource(ModelResource):
    
    class Meta:
        include_resource_uri = False
        queryset = RSSMessage.objects.all()
        resource_name = 'rss'
        serializer = Serializer(["json"])
        ordering = ['date',]

class InstagramResource(ModelResource):
    class Meta:
        include_resource_uri = False
        queryset = InstagramMessage.objects.all()
        resource_name = 'instagram'
        serializer = Serializer(["json"])
        ordering = ['date',]