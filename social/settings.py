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

class LazyAttribute(object):
    def __init__(self, model, attr):
        self._model = model
        self._attr  = attr

    def __getattribute__(self, attr):
        model = object.__getattribute__(self, '_model')
        model_attr = object.__getattribute__(self, '_attr')
        try:
            obj = model.objects.get()
        except model.DoesNotExist:
            obj = model()
        return getattr(getattr(obj, model_attr), attr)

    def __str__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__repr__()

    def __bool__(self):
        return self.__bool__()

    def __cmp__(self, other):
        return self.__cmp__(other)

    def __eq__(self, other):
        return self.__eq__(other)

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
