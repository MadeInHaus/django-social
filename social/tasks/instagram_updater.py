
import time
import gevent
from urlparse import urlparse, parse_qs
from .. import settings
from ..models import InstagramSearch, InstagramMessage, IGMediaExistsError
from ..services.instagram import InstagramAPI
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)






class InstagramUpdater():
    def __init__(self, api):
        self.api = api


    def update(self):
        import gevent.monkey
        gevent.monkey.patch_ssl()
        threads = []
        terms = InstagramSearch.objects.all()

        for term in terms:
            max_id = InstagramMessage.objects.filter(instagram_search__search_term=term.search_term)
            max_id = max_id[0] if len(max_id) else 0;
            print(max_id)
            threads.append(gevent.spawn(self._step, term))
        gevent.joinall(threads)

    def _step(self, term, max_id=0):
        try:
            log.warning('[instagram] term %s', term.search_term)
            log.warning('[instagram] max_id %s', max_id)
            response = self.api.tag_recent_media(term.search_term,max_id)
        except:
            log.error('crap')
            return
        max_id = response.get('pagination',{}).get('next_max_tag_id',0)
        medias = response.get('data',{})
        if(len(medias) == 0):
            log.warning('[instagram] no media for term %s with max_id %s',term.search_term, max_id)
        
        for media in medias:
            try:
                ig_media = InstagramMessage.create_from_json(media,term)
            except IGMediaExistsError:
                log.warning('[instagram] item already exists')
                return
            except Exception as e:
                log.error('[instagram ERROR] something went really wrong while saving')
                log.error(e)
                return

        # step through next page(s)
        self._step(term, max_id)
        

