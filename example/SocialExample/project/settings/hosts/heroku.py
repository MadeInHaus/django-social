from settings import *
import dj_database_url

DEBUG = False

print "Using Heroku Settings"


DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost'),
}

# this setting can be removed after setting up a static file serve through a cdn
SERVE_STATIC = True
