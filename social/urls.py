from django.conf.urls.defaults import include, patterns

from tastypie.api import Api
from social.api.resources import MessageResource, SocialResource, TwitterResource, FacebookResource

v1_api = Api(api_name='v1')
v1_api.register(MessageResource())
v1_api.register(SocialResource())
v1_api.register(TwitterResource())
v1_api.register(FacebookResource())

urlpatterns = patterns('',
    # API
    (r'^', include(v1_api.urls)),
)