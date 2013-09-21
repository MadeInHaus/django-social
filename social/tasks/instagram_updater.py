import gevent

from celery.utils.log import get_task_logger

from .. import settings
from ..models import InstagramAccount, InstagramSearch, InstagramMessage, IGMediaExistsError
from ..services.instagram import InstagramAPI, RateLimitException

log = get_task_logger(__name__)


class InstagramUpdater():
    def __init__(self):
        self._accounts = InstagramAccount.objects.all()

    def update(self):
        import gevent.monkey
        gevent.monkey.patch_ssl()

        self._update_accounts()
        self._update_terms()

    def _update_accounts(self):
        threads = []

        for account in self._accounts.filter(scrap_profile=True):
            threads.append(gevent.spawn(self._update_account, account))
        gevent.joinall(threads)

    def _update_terms(self):
        threads = []
        tags = InstagramSearch.objects.all()

        for tag in tags:
            threads.append(gevent.spawn(self._update_tag, tag))
        gevent.joinall(threads)

    def _update_account(self, account):
        log.info('[instagram] updating account "%s"'.format(account.username))

        api = InstagramAPI(account)
        try:
            self._iterate_messages(api.scrap_account)
        except RateLimitException:
                log.error('[instagram] account "{}" rate limited'.format(account.username))
        except Exception as exc:
            log.error('[instagram] error scraping account "{}"'.format(account.username))
            log.error(exc)

    def _iterate_messages(self, api_method, arguments=[], tag=None):
        message_duplicates = 0
        for message in api_method(*arguments):
            try:
                InstagramMessage.create_from_json(message, tag)
            except IGMediaExistsError:
                message_duplicates += 1
                if message_duplicates >= 5:
                    log.warning('[instagram] you hit 5 duplicates in a row, kicking out')
                    return
            else:
                # Reboot dup count as the last message was successfully
                # saved.
                message_duplicates = 0

    def _update_tag(self, tag):
        log.info('[instagram] searching for tag "%s"'.format(tag.search_term))

        for account in self._accounts:
            api = InstagramAPI(account)
            try:
                self._iterate_messages(api.search_tag, [tag.search_term], tag)
            except RateLimitException:
                log.error('[instagram] account "{}" rate limited'.format(account.username))
            except Exception as exc:
                log.error('[instagram] error searching for "{}"'.format(tag.search_term))
                log.error('[instagram] account "{}"'.format(account.username))
                log.error(exc)
                return
            else:
                return
