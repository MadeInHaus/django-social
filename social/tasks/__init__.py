from .. import settings
from datetime import timedelta, datetime
from celery.utils.log import get_task_logger
from celery import task
from celery.task import periodic_task
from .facebook import FacebookUpdater
from .twitter import TwitterUpdater


#@periodic_task(run_every=timedelta(minutes=settings.SOCIAL_FACEBOOK_INTERVAL))
@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_FACEBOOK_INTERVAL))
def twitter():
    log = get_task_logger('twitter')
    log.info('[Twitter] Start')
    tw = TwitterUpdater()
    tw.update()
    log.info('[Twitter] End')


@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_FACEBOOK_INTERVAL))
def facebook():
    log = get_task_logger('facebook')
    log.info('[Facebook] Start')
    fb = FacebookUpdater()
    fb.update()
    log.info('[Facebook] End')