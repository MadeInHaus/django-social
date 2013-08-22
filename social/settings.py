import operator
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


def new_method_proxy(func):
    def inner(self, *args):
        return func(self._wrapped_attribute, *args)
    return inner

class LazyAttribute(object):
    def __init__(self, model, attr):
        self._model = model
        self._attr  = attr

    @property
    def _wrapped_attribute(self):
        try:
            obj = self._model.objects.get()
        except self._model.DoesNotExist:
            obj = self._model()
        return getattr(obj, self._attr)

    __getattr__ = new_method_proxy(getattr)
    __str__ = new_method_proxy(str)
    __unicode__ = new_method_proxy(unicode)
    __repr__ = new_method_proxy(repr)
    __len__ = new_method_proxy(len)
    __iter__ = new_method_proxy(iter)
    __bool__ = new_method_proxy(bool)
    __nonzero__ = __bool__
    __cmp__ = new_method_proxy(cmp)
    __eq__ = new_method_proxy(operator.eq)
    __class__ = property(new_method_proxy(operator.attrgetter('__class__')))
    __hash__ = new_method_proxy(hash)
    __dir__ = new_method_proxy(dir)
    __reduce__ = new_method_proxy(reduce)
    __members__ = property(lambda self: self.__dir__())

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
