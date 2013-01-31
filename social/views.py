



def begin_auth(request):
    twitter = Twython(
        twitter_token = settings.TWITTER_KEY,
        twitter_secret = settings.TWITTER_SECRET,
        callback_url = request.build_absolute_uri(reverse('twitter_oauth.views.thanks'))
    )

    try:
        auth_props = twitter.get_authentication_tokens()
    except:
        print sys.exc_info()
        traceback.print_exc()
        pass
    
    request.session['request_token'] = auth_props
    return HttpResponseRedirect(auth_props['auth_url'])

def thanks(request, redirect_url=settings.LOGIN_REDIRECT_URL):
    twitter = Twython(
        twitter_token = settings.TWITTER_KEY,
        twitter_secret = settings.TWITTER_SECRET,
        oauth_token = request.session['request_token']['oauth_token'],
        oauth_token_secret = request.session['request_token']['oauth_token_secret'],
    )

    authorized_tokens = twitter.get_authorized_tokens()
    try:
        user = User.objects.get(username = authorized_tokens['screen_name'])
        user.set_password(authorized_tokens['oauth_token_secret'])
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(authorized_tokens['screen_name'], "", authorized_tokens['oauth_token_secret'])
        profile_info = twitter.showUser(screen_name=authorized_tokens['screen_name'])
        profile = TwitterProfile()
        profile.user                    = user
        profile.twitter_id              = profile_info['id']
        profile.screen_name             = profile_info['screen_name']
        profile.name                    = profile_info['name']
        profile.location                = profile_info['location']
        profile.profile_image_url       = profile_info['profile_image_url']
        profile.profile_image_url_https = profile_info['profile_image_url_https']
        profile.verified                = profile_info['verified']
        profile.friends_count           = profile_info['friends_count']
        profile.statuses_count          = profile_info['statuses_count']
        profile.oauth_token             = authorized_tokens['oauth_token']
        profile.oauth_secret            = authorized_tokens['oauth_token_secret']
        profile.save()

    user = authenticate(
        username = authorized_tokens['screen_name'],
        password = authorized_tokens['oauth_token_secret']
    )
    # user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect(redirect_url)
