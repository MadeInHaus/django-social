from django.contrib import admin

from django.template.response import TemplateResponse

from .models import FacebookAccount, FacebookMessage, TwitterAccount, TwitterMessage,\
                    TwitterSearch, RSSAccount, RSSMessage, Message, InstagramSearch, InstagramMessage
from .settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET
from .views import begin_auth

from logging import getLogger
from django.http import HttpResponseRedirect
import traceback
from twython.twython import Twython
from django.core.urlresolvers import reverse

log = getLogger(__name__)


def approve_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = 1
        item.save()
approve_message.short_description = "Mark As Approved"

def rejected_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = 2
        item.save()
rejected_message.short_description = "Mark As Rejected"

def favorite_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = 5
        item.save()
favorite_message.short_description = "Mark As Favorite"

class MessageAdmin(admin.ModelAdmin):
    actions = [approve_message, rejected_message, favorite_message]

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)
    
    def add_view(self, request, form_url='', extra_context=None):
        log.debug("request: %s", request)
        log.debug("form_url: %s", form_url)
        log.debug("extra_context: %s", extra_context)
        return begin_auth(request)

class TwitterMessageAdmin(MessageAdmin):
    list_display = ('id','message', 'status')
    list_filter = ('twitter_search__search_term', 'twitter_account__screen_name')

class MessageAdmin(MessageAdmin):
    list_display = ('id','message', 'status')
    list_filter = ('network', )

class InstagramMessageAdmin(MessageAdmin):
    list_display = ('id','admin_image_low','message', 'status')


admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage, MessageAdmin)
admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterMessage, TwitterMessageAdmin)
admin.site.register(TwitterSearch)
admin.site.register(InstagramSearch)
admin.site.register(InstagramMessage, InstagramMessageAdmin)
admin.site.register(Message, MessageAdmin)



class RSSMessageAdmin(admin.ModelAdmin):
    list_display = ('id','message')
    list_filter = ('rss_account__feed_name', )

admin.site.register(RSSAccount)
admin.site.register(RSSMessage, RSSMessageAdmin)
