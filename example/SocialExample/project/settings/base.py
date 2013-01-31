import os.path
import sys

import djcelery

# Include apps on the path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APPS_ROOT = os.path.join(PROJECT_ROOT, "apps")
if APPS_ROOT not in sys.path:
    sys.path.insert(0, APPS_ROOT)

# People who get code error notifications when DEBUG=False
ADMINS = (('Social Example App administrator', 'cms-admin@madeinhaus.com'),)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'django',            
        'USER': 'vagrant',                      
        'PASSWORD': 'vagrant',                  
        'HOST': '',                      
        'PORT': '',                      
    }
}

# CELERY SETTINGS
djcelery.setup_loader()
CELERY_RESULT_BACKEND = 'amqp'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# SOCIAL SETTINGS
SOCIAL_FACEBOOK_APP_ID = '399154676843137'
SOCIAL_FACEBOOK_APP_SECRET = '5fa53aec57af082659fe74c51a3555ca'

SOCIAL_TWITTER_CONSUMER_KEY = 'GB6gSL7mojCQK8lJe5JEg'
SOCIAL_TWITTER_CONSUMER_SECRET = 'jhV32lskDKd4pZI9zDHsWrFXrQmakUApIGOANsd7g'

SOCIAL_FACEBOOK_INTERVAL = 1*60
SOCIAL_TWITTER_INTERVAL = 1*60


# REDIS SETTINGS
REDIS_HOST = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Never deploy a site into production with DEBUG turned on!
DEBUG = True

# Address to use for various automated correspondence from the site manager(s).
DEFAULT_FROM_EMAIL = 'cms-admin@madeinhaus.com'

# Set the subject prefix for email messages sent to admins and managers
EMAIL_SUBJECT_PREFIX = '[Social Example App]'

#DEFAULT_FROM_EMAIL = ''
#EMAIL_HOST = ''
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True

# Maximum size (in bytes) before an upload gets streamed to the file system.
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# List of locations of the fixture data files, in search order
FIXTURE_DIRS = ()

# A tuple of strings designating all the enabled applications
INSTALLED_APPS = (
    'grappelli',
    
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'require',
    #'debug-toolbar',
    'gunicorn',
    'tastypie',
    'djcelery',
    'south',
    
    'utils',
    'social',
    
)

# A tuple of IP addresses that see debug comments, when DEBUG is True
INTERNAL_IPS = ('0.0.0.0', '127.0.0.1',)

#Secure proxy setting 
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_SSL_PROXY', 'true')

# The language code for this installation
LANGUAGE_CODE = 'en-us'

# If login is successful, the view redirects to the URL specified in next.
# If next isn't provided, it redirects to settings.LOGIN_REDIRECT_URL
# (which defaults to /accounts/profile/).
LOGIN_REDIRECT_URL = '/admin'

# Who should get broken-link notifications when SEND_BROKEN_LINK_EMAILS=True
MANAGERS = ADMINS

# Absolute path to the directory that holds stored files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT (must end in a slash)
MEDIA_URL = '/uploads/'

# A tuple of middleware classes to use
MIDDLEWARE_CLASSES = (
    # Site Optimization Middleware
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',

    # Common Middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Debug
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    
)


APPEND_SLASH = True

# Number of digits grouped together on the integer part of a number
NUMBER_GROUPING = 3

# The full Python import path to the root URLconf
ROOT_URLCONF = 'urls'

# Seed for secret-key hashing algorithms
SECRET_KEY = 'ydbujgrh09qn3xufjq8jkc2hlm7tr9oguofnhp0hurq39dyjmt'

# Whether files other than .html should be returned with the correct MIME type
SET_MIMETYPE = True

# The ID of the current site in the django_site database table
SITE_ID = 1


# Absolute path to the directory where collectstatic will collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'collected-static')

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# see django-require if S3 is required https://github.com/etianen/django-require
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

#should be off on production
SERVE_STATIC = True

# Additional locations the staticfiles app will traverse

DEV_STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (DEV_STATIC_ROOT,)

# The Site Title of your Admin-Interface. Change this instead of changing index.html
GRAPPELLI_ADMIN_TITLE = "Social Example App"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    
)

# Display a detailed report for any TemplateSyntaxError.
TEMPLATE_DEBUG = DEBUG

# List of locations of the template source files, in search order
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# A tuple of template loader classes, specified as strings
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# The time zone for this installation
TIME_ZONE = None  #'America/Los_Angeles'

# Output the "Etag" header. This saves bandwidth but slows down performance
USE_ETAGS = False

# Enable Django's internationalization system
USE_I18N = False

# Display numbers and dates using the format of the current locale
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Testing
TEST_RUNNER = 'testing.TestRunner'

# Which settings are passed by RequestContext to the templates
# Keep this list small, as it is passed to each request.
# Uncomment more settings as needed
VIEW_SETTINGS = (
    'LANGUAGE_CODE',
    'TEMPLATE_DEBUG',
    'PERM_STATIC_URL'
)

LOG_FILENAME = None


# Django Require settings

# The baseUrl to pass to the r.js optimizer.
REQUIRE_BASE_URL = "js"

# The name of a build profile to use for your project, relative to REQUIRE_BASE_URL.
# A sensible value would be 'app.build.js'. Leave blank to use the built-in default build profile.
REQUIRE_BUILD_PROFILE = "app.build.js"

# The name of the require.js script used by your project, relative to REQUIRE_BASE_URL.
REQUIRE_JS = "libs/require.js"

# A dictionary of standalone modules to build with almond.js.
# See the section on Standalone Modules, below.
REQUIRE_STANDALONE_MODULES = {}

# Whether to run django-require in debug mode.
REQUIRE_DEBUG = False

# A tuple of files to exclude from the compilation result of r.js.
REQUIRE_EXCLUDE = ("build.txt",)

# The execution environment in which to run r.js: node or rhino.
REQUIRE_ENVIRONMENT = "node"

# Debug toolbar settings
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

def custom_show_toolbar(request):
    return True  # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
    'ENABLE_STACKTRACES' : True,
}
