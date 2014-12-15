import gevent

from celery.utils.log import get_task_logger

from .. import settings
from ..models import InstagramAccount, InstagramSearch, InstagramMessage, \
    IGUserFiltered, IGMediaExistsError, InstagramPublicAccount, InstagramSetting, \
    IGTermFiltered
from ..services.instagram import InstagramAPI, RateLimitException, InstagramPublicAPI

log = get_task_logger(__name__)

MAX_DUPLICATES = 20


class InstagramUpdater():
    def __init__(self):
        self._accounts = InstagramAccount.objects.all()

    def update(self):
        import gevent.monkey
        gevent.monkey.patch_ssl()

        self._update_accounts()
        self._update_public_accounts()
        self._update_terms()

    def _update_accounts(self):
        threads = []

        for account in self._accounts.filter(scrape_profile=True):
            threads.append(gevent.spawn(self._update_account, account))
        gevent.joinall(threads)

    def _update_public_accounts(self):
        threads = []

        for account in InstagramPublicAccount.objects.all():
            threads.append(gevent.spawn(self._update_public_account, account))
        gevent.joinall(threads)

    def _update_terms(self):
        threads = []
        tags = InstagramSearch.objects.all()

        for tag in tags:
            threads.append(gevent.spawn(self._update_tag, tag))
        gevent.joinall(threads)

    def _update_account(self, account):
        log.info('[instagram] updating account "{}"'.format(account.username))

        api = InstagramAPI(account)
        try:
            self._iterate_messages(api.scrape_account)
        except RateLimitException:
                log.error('[instagram] account "{}" rate limited'.format(account.username))
        except Exception:
            log.exception('[instagram] error scraping account "{}"'.format(account.username))

    def _update_public_account(self, account):
        log.info('[instagram] updating public account "{}"'.format(account.username))

        api = InstagramPublicAPI(InstagramSetting.objects.get())
        try:
            self._iterate_messages(api.scrape_public_account, arguments=[account,])
        except RateLimitException:
            log.error('[instagram] public account "{}" rate limited'.format(account.username))
        except Exception:
            log.exception('[instagram] error scraping public account "{}"'.format(account.username))


    def _iterate_messages(self, api_method, arguments=[], tag=None, filter_users=None):
        message_duplicates = 0
        last_id = tag.last_id if tag else None
        for message in api_method(*arguments):
            try:
                msg = InstagramMessage.create_from_json(message, tag, filter_users=filter_users)
                last_id = msg.message_id if last_id is None or msg.message_id > last_id else last_id
            except IGMediaExistsError:
                message_duplicates += 1
                if message_duplicates >= MAX_DUPLICATES:
                    log.warning('[instagram] you hit {} duplicates in a row, kicking out'.format(MAX_DUPLICATES))
                    return last_id
            except IGUserFiltered:
                pass # ignore filtered users...
            except IGTermFiltered:
                pass # ignore filtered search messages
            else:
                # Reboot dup count as the last message was successfully
                # saved.
                message_duplicates = 0
        return last_id

    def _update_tag(self, tag):
        log.info('[instagram] searching for tag "{}"'.format(tag.search_term))

        filter_users = [tag.username] if tag.username else None

        api = InstagramPublicAPI(InstagramSetting.objects.get())

        try:
            last_id = self._iterate_messages(api.search_tag, [tag], tag, filter_users=filter_users)
            if tag:
                tag.last_id = last_id
                tag.save()
        except RateLimitException:
            log.error('[instagram] rate limited during tag "{}"'.format(tag.search_term))
        except Exception as exc:
            log.error('[instagram] error searching for "{}"'.format(tag.search_term))
            log.error(exc)
            return
        else:
            return
