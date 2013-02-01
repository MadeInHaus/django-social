import sys
import traceback

from twython import Twython
from django.core.urlresolvers import reverse

from logging import getLogger
from django.http import HttpResponseRedirect


from .settings import SOCIAL_TWITTER_CONSUMER_KEY, SOCIAL_TWITTER_CONSUMER_SECRET
from .models import TwitterAccount

log = getLogger('social.views')

def begin_auth(request):
    twitter = Twython(
        twitter_token = SOCIAL_TWITTER_CONSUMER_KEY,
        twitter_secret = SOCIAL_TWITTER_CONSUMER_SECRET,
        callback_url = request.build_absolute_uri(reverse('social.views.thanks'))
    )

    try:
        auth_props = twitter.get_authentication_tokens()
    except:
        log.error(traceback.format_exc())
        log.error(traceback.format_stack())
    
    request.session['request_token'] = auth_props
    
    return HttpResponseRedirect(auth_props['auth_url'])

def thanks(request, redirect_url='/admin/social/twitteraccount/'):
    twitter = Twython(
        twitter_token = SOCIAL_TWITTER_CONSUMER_KEY,
        twitter_secret = SOCIAL_TWITTER_CONSUMER_SECRET,
        oauth_token = request.session['request_token']['oauth_token'],
        oauth_token_secret = request.session['request_token']['oauth_token_secret'],
    )

    authorized_tokens = twitter.get_authorized_tokens()
    log.error("authorized_tokens: {}".format(authorized_tokens))
    
    try:
        account = TwitterAccount.objects.get(screen_name=authorized_tokens['screen_name'])
        account.oauth_token             = authorized_tokens['oauth_token']
        account.oauth_secret            = authorized_tokens['oauth_token_secret']
        account.save()
    except TwitterAccount.DoesNotExist:
        account = TwitterAccount()
        account_info = twitter.showUser(screen_name=authorized_tokens['screen_name'])
        account.user_id                 = unicode(account_info['id'])
        account.twitter_id              = account_info['id']
        account.screen_name             = account_info['screen_name']
        account.user_name               = account_info['name']
        account.location                = account_info['location']
        account.avatar                  = account_info['profile_image_url']
        account.profile_image_url_https = account_info['profile_image_url_https']
        account.verified                = account_info['verified']
        account.friends_count           = account_info['friends_count']
        account.statuses_count          = account_info['statuses_count']
        account.oauth_token             = authorized_tokens['oauth_token']
        account.oauth_secret            = authorized_tokens['oauth_token_secret']
        account.save()

    return HttpResponseRedirect(redirect_url)
