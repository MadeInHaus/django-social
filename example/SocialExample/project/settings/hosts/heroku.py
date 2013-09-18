from settings import *
import dj_database_url
import sys

import os

from json import load

DEBUG = False

print >> sys.stderr, "Using Heroku Settings"

try:
    APP_INFO = load(open(BASE_DIR + "/app_info.json"))['prod']
except:
    print "Failed to load app_info.json"
    APP_INFO = {}

print "using appinfo: ", APP_INFO


DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost'),
}

DATABASES['default']['ENGINE'] = 'django_postgrespool'


# this setting can be set to False after setting up a static file serve through a cdn
SERVE_STATIC = True

# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('HAUS_AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('HAUS_AWS_SECRET_ACCESS_KEY','')

AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME = 'django-social-example'

# suppress bucket auth via accesskeys
AWS_QUERYSTRING_AUTH = False

STATICFILES_STORAGE = 'utils.storage.OptimizedS3BotoStorage'
DEFAULT_FILE_STORAGE = "utils.storage.MediaRootS3BotoStorage"

ASSET_PROTOCOL = 'https' if USE_HTTPS_FOR_ASSETS else 'http'

STATIC_URL = '{}://s3.amazonaws.com/{}/'.format(ASSET_PROTOCOL, AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = '{}://s3.amazonaws.com/{}/uploads/'.format(ASSET_PROTOCOL, AWS_STORAGE_BUCKET_NAME)

INSTALLED_APPS += ('storages',)

ALLOWED_HOSTS += ('{}.herokuapp.com'.format(APP_INFO.get('heroku_app_name','')), )