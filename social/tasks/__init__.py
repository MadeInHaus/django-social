from .. import settings
from datetime import timedelta, datetime
from celery.utils.log import get_task_logger
from celery import task
from celery.task import periodic_task
from .facebook_updater import FacebookUpdater
from .twitter_updater import TwitterUpdater
from .rss_updater import RSSUpdater



#@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_TWITTER_INTERVAL))
@periodic_task(run_every=timedelta(seconds=15))
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

@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_RSS_INTERVAL))
def rss_update():
    log = get_task_logger('rss')
    log.info('[RSS] Start')
    rss = RSSUpdater()
    rss.update()
    log.info('[RSS] End')
    
