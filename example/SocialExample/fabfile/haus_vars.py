import functools

from json import load
from fabric.colors import red, yellow
from fabric.api import abort, cd, run

from fabric.context_managers import shell_env


import os

import logging
logging.basicConfig()
log = logging.getLogger(__name__)

# Load/parse app_info.json
try:
    APP_INFO = load(open("app_info.json"))
except:
    print red("Failed to load app_info.json")
    abort()

# suppress tasks
__all__ = []


def parse_vars(string):
    """Parse a list of var/values separated by \\n"""
    d = {}
    for line in string.split('\n'):
        if '=' not in line:
            continue
        name, value = line.strip().split('=')
        value = value.strip('"')
        d[name] = value
    return d


def get_haus_vars():
    """parse environment vars for variables starting with HAUS"""
    haus_vars = {}
    for k in os.environ:
        if k.startswith('HAUS'):
            haus_vars[k] = os.environ[k]
    return haus_vars

HAUS_VARS = get_haus_vars()

def get_static_url(d):
    """grab STATIC_URL from django settings"""
    with shell_env(**d):
        with cd("/var/www"):
            settings = parse_vars(run("./manage.py settings_vars STATIC_URL"))
            if 'STATIC_URL' not in settings:
                log.error('STATIC_URL lookup failed!!!')
                abort("STATIC_URL lookup failed!!!")
            return settings['STATIC_URL']

def with_vars(f):
    """Decorator adds HAUS_VARS to environment variables, if an env argument is passed the corresponding values from app_info.json will also be added to the env vars""" 
    @functools.wraps(f)
    def wrapper( *args, **kwargs ):
        d = {}
        d.update(HAUS_VARS)
        if 'env' in kwargs:
            d.update(APP_INFO[kwargs['env']])
            d['STATIC_URL'] = get_static_url(d)

        if 'asset_version' in kwargs:
            d['ASSET_VERSION'] = kwargs['asset_version']
        with shell_env(**d):
            print yellow('using vars: {}'.format(d))
            return f( *args, **kwargs )
    return wrapper

