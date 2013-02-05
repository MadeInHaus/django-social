from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

from social.models import Message, TwitterMessage, FacebookMessage

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
