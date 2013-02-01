from django.contrib import admin

from django.template.response import TemplateResponse

from .models import FacebookAccount, FacebookMessage, TwitterAccount, TwitterMessage, RSSAccount, RSSMessage
from .settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET
from .views import begin_auth

from logging import getLogger
from django.http import HttpResponseRedirect
import traceback
from twython.twython import Twython
from django.core.urlresolvers import reverse

log = getLogger("social.admin")

admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage)

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)
    
    def add_view(self, request, form_url='', extra_context=None):
        log.debug("request: {}".format(request))
        log.debug("form_url: {}".format(form_url))
        log.debug("extra_context: {}".format(extra_context))

        return begin_auth(request)

admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterMessage)

admin.site.register(RSSAccount)
admin.site.register(RSSMessage)
