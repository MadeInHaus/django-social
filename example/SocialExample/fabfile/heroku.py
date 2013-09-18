from fabric.api import local, run, cd, abort
from fabric.tasks import Task
from fabric.context_managers import shell_env

from vagrant import collectstatic, css_compile, killall
from fabric.colors import red, green, yellow

from haus_vars import with_vars, APP_INFO


import logging
logging.basicConfig()
log = logging.getLogger(__name__)

# suppress tasks
__all__ = []


def compile_env_css():
    log.warning(red('Calling killall,  all process will be killed!'))
    killall()
    css_compile()
    log.warning(red('Note killall was called so vagrant server/compass will be down'))


def get_hash(env):
    print red("CHECKING OUT BRANCH: {}".format(APP_INFO[env]["branch_name"]))
    local('git checkout {}'.format(APP_INFO[env]["branch_name"]))
    return local('git rev-parse HEAD', capture=True).strip()[:20]


def get_heroku_asset_version(env):
    git_hash = local('heroku config:get ASSET_VERSION -a {}'.format(APP_INFO[env]["heroku_app_name"]), capture=True)
    print "got hash: ", yellow('{}'.format(git_hash))
    return git_hash


def set_heroku_asset_version(env, git_hash):
    local('heroku config:set ASSET_VERSION={} -a {}'.format(git_hash, APP_INFO[env]["heroku_app_name"]))


def current_asset_version(env, ):
    return get_hash(env)



class CustomTask(Task):
    roles = ['vagrant']
    
    def __init__(self, func, env, *args, **kwargs):
        super(CustomTask, self).__init__(*args, **kwargs)
        self.func = func
        self.env = env
        self.name = func.__name__
        self.__doc__ = func.__doc__

    def run(self, *args, **kwargs):
        if 'env' not in kwargs:
            kwargs['env'] = self.env
        return self.func(*args, **kwargs)



@with_vars
def deploy(env=None, ):
    """Deploy static and source to heroku environment"""
    compile_env_css()
    version = current_asset_version(env=env)
    deploy_static_media(env=env, asset_version=version)
    deploy_source(env=env, asset_version=version)


@with_vars
def deploy_source(env=None, asset_version=''):
    """Deploy source to heroku environment"""
    print green('Deploying source to Heroku')
    local('git push {} {}:master'.format(APP_INFO[env]["heroku_remote_name"], APP_INFO[env]["branch_name"]))
    sync_prod_db(env=env)
    set_heroku_asset_version(env, asset_version)


@with_vars
def deploy_static_media(env=None, asset_version=''):
    """Deploy static (runs collectstatic within given environment)"""
    print green('Deploying static media')
    collectstatic(no_input=True)


@with_vars
def deploy_user_media(env=None ):
    """Deploy user media to media location on s3"""
    print green('Deploying user media')
    with cd("/var/www"):
        run('./manage.py sync_media_s3 --prefix=uploads')


@with_vars
def sync_prod_db(env=None, reset_db=False):
    """Run syncdb and migrate within given environment"""
    print green('sync/migrate DB')
    if reset_db:
        # uncomment below and replace DATABSE_URL with the prod database url
        # note that this is destructive of the PROD DB
        #local('heroku pg:reset DATABASE_URL') #add "--confirm haus" to remove required input
        pass
    local('heroku run ./manage.py syncdb -a {}'.format(APP_INFO[env]["heroku_app_name"]))
    local('heroku run ./manage.py migrate -a {}'.format(APP_INFO[env]["heroku_app_name"]))

