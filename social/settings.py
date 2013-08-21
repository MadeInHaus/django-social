from .models import TwitterSetting, FacebookSetting, InstagramSetting, RSSSetting

__all__ = (
    'SOCIAL_TWITTER_AUTO_APPROVE',
    'SOCIAL_TWITTER_INTERVAL',
    'SOCIAL_TWITTER_CONSUMER_KEY',
    'SOCIAL_TWITTER_CONSUMER_SECRET',

    'SOCIAL_FACEBOOK_AUTO_APPROVE',
    'SOCIAL_FACEBOOK_INTERVAL',
    'SOCIAL_FACEBOOK_APP_ID',
    'SOCIAL_FACEBOOK_APP_SECRET',

    'SOCIAL_INSTAGRAM_AUTO_APPROVE',
    'SOCIAL_INSTAGRAM_INTERVAL',
    'SOCIAL_INSTAGRAM_CLIENT_ID',
    'SOCIAL_INSTAGRAM_CLIENT_SECRET',
    'SOCIAL_INSTAGRAM_REDIRECT_URI',

    'SOCIAL_RSS_AUTO_APPROVE',
    'SOCIAL_RSS_INTERVAL',
)

class LazyAttribute:
    def __init__(self, model, attr):
        self._model = model
        self._attr  = attr

    def _wrapped_attribute(self):
        try:
            obj = self._model.objects.get()
        except model.DoesNotExist:
            obj = self._model()
        return getattr(obj, self._attr)

    def __getattr__(self, name):
        return getattr(self._wrapped_attribute(), name)

SOCIAL_TWITTER_AUTO_APPROVE    = LazyAttribute(TwitterSetting, 'auto_approve')
SOCIAL_TWITTER_INTERVAL        = LazyAttribute(TwitterSetting, 'interval')
SOCIAL_TWITTER_CONSUMER_KEY    = LazyAttribute(TwitterSetting, 'consumer_key')
SOCIAL_TWITTER_CONSUMER_SECRET = LazyAttribute(TwitterSetting, 'consumer_secret')

SOCIAL_FACEBOOK_AUTO_APPROVE = LazyAttribute(FacebookSetting, 'auto_approve')
SOCIAL_FACEBOOK_INTERVAL     = LazyAttribute(FacebookSetting, 'interval')
SOCIAL_FACEBOOK_APP_ID       = LazyAttribute(FacebookSetting, 'app_id')
SOCIAL_FACEBOOK_APP_SECRET   = LazyAttribute(FacebookSetting, 'app_secret')

SOCIAL_INSTAGRAM_AUTO_APPROVE  = LazyAttribute(InstagramSetting, 'auto_approve')
SOCIAL_INSTAGRAM_INTERVAL      = LazyAttribute(InstagramSetting, 'interval')
SOCIAL_INSTAGRAM_CLIENT_ID     = LazyAttribute(InstagramSetting, 'client_id')
SOCIAL_INSTAGRAM_CLIENT_SECRET = LazyAttribute(InstagramSetting, 'client_secret')
SOCIAL_INSTAGRAM_REDIRECT_URI  = LazyAttribute(InstagramSetting, 'redirect_uri')

SOCIAL_RSS_AUTO_APPROVE = LazyAttribute(RSSSetting, 'auto_approve')
SOCIAL_RSS_INTERVAL     = LazyAttribute(RSSSetting, 'interval')
