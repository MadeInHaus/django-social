from django.conf.urls.defaults import patterns

from social.views import thanks, instauth
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'thanks/', thanks, name="twitter_callback"),
    url(r'instauth/', instauth, name="instagram_callback"),
)
