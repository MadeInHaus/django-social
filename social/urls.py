from django.conf.urls.defaults import patterns

from social.views import thanks
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'^thanks/', thanks, name="twitter_callback"),
)
