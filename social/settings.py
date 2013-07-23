from .models import TwitterSetting, FacebookSetting, InstagramSetting, RSSSetting

__all__ = (
    'SOCIAL_TWITTER_AUTO_APPROVE',
    'SOCIAL_FACEBOOK_AUTO_APPROVE',
    'SOCIAL_INSTAGRAM_AUTO_APPROVE',
    'SOCIAL_RSS_AUTO_APPROVE',
    'SOCIAL_TWITTER_INTERVAL',
    'SOCIAL_FACEBOOK_INTERVAL',
    'SOCIAL_INSTAGRAM_INTERVAL',
    'SOCIAL_RSS_INTERVAL',
    'SOCIAL_FACEBOOK_APP_ID',
    'SOCIAL_FACEBOOK_APP_SECRET',
    'SOCIAL_TWITTER_CONSUMER_KEY',
    'SOCIAL_TWITTER_CONSUMER_SECRET',
    'SOCIAL_INSTAGRAM_CLIENT_ID',
    'SOCIAL_INSTAGRAM_CLIENT_SECRET',
)


def get_or_create(model):
    try:
        return model.objects.get()
    except model.DoesNotExist:
        return model()

twitter = get_or_create(TwitterSetting)
facebook = get_or_create(FacebookSetting)
instagram = get_or_create(InstagramSetting)
rss = get_or_create(RSSSetting)


SOCIAL_TWITTER_AUTO_APPROVE = twitter.auto_approve
SOCIAL_FACEBOOK_AUTO_APPROVE = facebook.auto_approve
SOCIAL_INSTAGRAM_AUTO_APPROVE = instagram.auto_approve
SOCIAL_RSS_AUTO_APPROVE = rss.auto_approve

SOCIAL_TWITTER_INTERVAL = twitter.interval
SOCIAL_FACEBOOK_INTERVAL = facebook.interval
SOCIAL_INSTAGRAM_INTERVAL = instagram.interval
SOCIAL_RSS_INTERVAL = rss.interval

SOCIAL_FACEBOOK_APP_ID = facebook.app_id
SOCIAL_FACEBOOK_APP_SECRET = facebook.app_secret

SOCIAL_TWITTER_CONSUMER_KEY = twitter.consumer_key
SOCIAL_TWITTER_CONSUMER_SECRET = twitter.consumer_secret

SOCIAL_INSTAGRAM_CLIENT_ID = instagram.client_id
SOCIAL_INSTAGRAM_CLIENT_SECRET = instagram.client_secret
