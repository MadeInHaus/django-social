from . import settings
from celery.utils.log import get_task_logger
from celery import task
from celery.task import periodic_task
from .facebook import FacebookUpdate
from .twitter import TwitterUpdate


@periodic_task(run_every=timedelta(minutes=settings.SOCIAL_FACEBOOK_INTERVAL))
def twitter(show):
    log = get_task_logger('twitter')
    log.info('[Twitter] Start')
    #update twitter
    log.info('[Twitter] End')


@periodic_task(run_every=timedelta(minutes=settings.SOCIAL_TWITTER_INTERVAL))
def facebook(show):
    log = get_task_logger('facebook')
    log.info('[Facebook] Start')
    #update facebook
    log.info('[Facebook] End')