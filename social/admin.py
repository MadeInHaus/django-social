from django.contrib import admin

from django.template.response import TemplateResponse

from .models import FacebookAccount, FacebookMessage, TwitterAccount, TwitterMessage, TwitterSearch, RSSAccount, RSSMessage, Message
from .settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET
from .views import begin_auth

from logging import getLogger
from django.http import HttpResponseRedirect
import traceback
from twython.twython import Twython
from django.core.urlresolvers import reverse

log = getLogger(__name__)

admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage)

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)
    
    def add_view(self, request, form_url='', extra_context=None):
        log.debug("request: %s", request)
        log.debug("form_url: %s", form_url)
        log.debug("extra_context: %s", extra_context)
        return begin_auth(request)

class TwitterMessageAdmin(admin.ModelAdmin):
    list_display = ('id','message')
    list_filter = ('twitter_search__search_term', 'twitter_account__screen_name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','message')
    list_filter = ('network', )

admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterMessage, TwitterMessageAdmin)
admin.site.register(TwitterSearch)
admin.site.register(Message, MessageAdmin)



class RSSMessageAdmin(admin.ModelAdmin):
    list_display = ('id','message')
    list_filter = ('rss_account__feed_name', )

admin.site.register(RSSAccount)
admin.site.register(RSSMessage, RSSMessageAdmin)
