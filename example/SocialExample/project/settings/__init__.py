import os.path
import sys

from base import *

# Load settings overides
_path = os.path.join(PROJECT_ROOT, 'settings', 'hosts')
sys.path.insert(0, _path)

from socket import gethostname
_hostname = gethostname().split('.')[0]

_overide_var = 'APP_ENV'
_overide_var = _overide_var.replace(' ', '_').upper()

if os.environ.get(_overide_var):
    sys.modules['host'] = __import__(os.environ.get(_overide_var))
    from host import *
    del sys.modules['host']
elif os.path.isfile(os.path.join(_path,'local_settings.py')):
    from local_settings import *
elif os.path.isfile(os.path.join(_path, '%s.py' % _hostname)):
    sys.modules['host'] = __import__(_hostname)
    from host import *
    del sys.modules['host']

sys.path.remove(_path)

# Any other configuration that should apply to all
# settings versions but relies on other settings (ie: debug)
# should go here.

# Email logging is off by default,  config variable must be set to enable
ENABLE_EMAIL_LOGGING = os.environ.get('ENABLE_EMAIL_LOGGING', 'NO') == 'YES'
ERROR_RATE_LIMIT = 60*10 # limit to one duplicate error every 10 minutes...

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
                                '()': 'django.utils.log.RequireDebugFalse'
                                },
        'ratelimit': {
                      '()': 'utils.error_ratelimit_filter.RateLimitFilter',
                      }
    },
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
           'filters': ['require_debug_false', 'ratelimit'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream' : {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file' : {
            'level' : 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME and LOG_FILENAME or '/dev/null',
            'formatter': 'verbose'
        }
    },
           
    'loggers': {
        '': {
            'handlers': ENABLE_EMAIL_LOGGING and ['stream', 'mail_admins'] or ['stream'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db': {
            'handlers': ENABLE_EMAIL_LOGGING and ['stream', 'mail_admins'] or ['stream'],
            'level': 'WARNING',
            'propagate': False,
        },
        'z.pool': {
            'handlers': ENABLE_EMAIL_LOGGING and ['stream', 'mail_admins'] or ['stream'],
            'level': 'WARNING',
            'propagate': False,
        },

    }
}

# URL That doesn't change.
PERM_STATIC_URL = STATIC_URL

# Include Asset Version in STATIC_URL
ASSET_VERSION = os.environ.get("ASSET_VERSION", None)
if ASSET_VERSION:
    AWS_LOCATION = '%s/' % ASSET_VERSION # set path of assets in s3 bucket, note this is '' by default
    STATIC_URL += AWS_LOCATION

