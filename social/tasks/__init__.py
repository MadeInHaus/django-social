from .. import settings
from ..services.facebook import FacebookAPI
from datetime import timedelta, datetime
from celery.utils.log import get_task_logger
from celery import task
from celery.task import periodic_task
from .facebook_updater import FacebookUpdater
from .twitter_updater import TwitterUpdater
from .rss_updater import RSSUpdater
from .instagram_updater import InstagramUpdater



@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_TWITTER_INTERVAL))
def twitter_update():
    log = get_task_logger('twitter')
    log.info('[Twitter] Start')
    tw = TwitterUpdater()
    tw.update()
    log.info('[Twitter] End')

@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_FACEBOOK_INTERVAL))
def facebook_update():
    log = get_task_logger('facebook')
    log.info('[Facebook] Start')
    fbapi = FacebookAPI(
            settings.SOCIAL_FACEBOOK_APP_ID,
            settings.SOCIAL_FACEBOOK_APP_SECRET)
    fb = FacebookUpdater(fbapi)
    fb.update()
    log.info('[Facebook] End')

@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_RSS_INTERVAL))
def rss_update():
    log = get_task_logger('rss')
    log.info('[RSS] Start')
    rss = RSSUpdater()
    rss.update()
    log.info('[RSS] End')
    
@periodic_task(run_every=timedelta(seconds=settings.SOCIAL_INSTAGRAM_INTERVAL))
def instagram_update():
    log = get_task_logger('instagram')
    log.info('[Instagram] Start')
    instagram = InstagramUpdater()
    instagram.update()
    log.info('[Instagram] End')