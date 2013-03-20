
import time
import gevent
from urlparse import urlparse, parse_qs
from .. import settings
from ..models import InstagramSearch, InstagramMessage, IGMediaExistsError
from ..services.instagram import InstagramAPI
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)






class InstagramUpdater():
    def __init__(self):
        self.api = InstagramAPI(app_id=settings.SOCIAL_INSTAGRAM_CLIENT_ID)


    def update(self):
        import gevent.monkey
        gevent.monkey.patch_ssl()
        threads = []
        terms = InstagramSearch.objects.all()

        for term in terms:
            threads.append(gevent.spawn(self._update_term, term))
        gevent.joinall(threads)

    def _update_term(self, term):
        try:
            log.warning('[instagram] term %s', term.search_term)
            messages = self.api.tag_recent_media(term.search_term)
        except Exception as e:
            log.error('[instagram] unkown error')
            log.error(e)
            return
        message_duplicates = 0
        for message in messages:
            try:
                InstagramMessage.create_from_json(message,term)
                message_duplicates = 0
            except IGMediaExistsError as e:
                message_duplicates += 1
                if message_duplicates > 5:
                    log.warning('[instagram] you hit 5 duplicates in a row, kicking out')
                    return
            except Exception as e:
                log.error('[instagrame] larger problem...')
                log.error(e)
                