from django.conf.urls.defaults import include, patterns

from tastypie.api import Api
from .api.resources import MessageResource, TwitterResource, FacebookResource
from social.views import thanks
from django.conf.urls import url

v1_api = Api(api_name='v1')
v1_api.register(MessageResource())
v1_api.register(TwitterResource())
v1_api.register(FacebookResource())

urlpatterns = patterns('',
    # API
    (r'^', include(v1_api.urls)),
    
    url(r'^thanks/', thanks, name="twitter_callback"),
)