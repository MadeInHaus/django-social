from django.conf import settings


TWITTER_AUTO_APPROVE = getattr(settings, 'TWITTER_AUTO_APPROVE', False)
FACEBOOK_AUTO_APPROVE = getattr(settings, 'FACEBOOK_AUTO_APPROVE', False)
