from urllib import urlencode
from logging import getLogger

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from ..settings import SOCIAL_INSTAGRAM_CLIENT_ID, SOCIAL_INSTAGRAM_REDIRECT_URI
from ..models import TwitterSetting, FacebookSetting, InstagramSetting, RSSSetting, \
                     APPROVED, PENDING, FAVORITED, REJECTED, LEGAL
from ..views import begin_auth


log = getLogger(__name__)


def approve_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = APPROVED
        item.save()
approve_message.short_description = "Mark As Approved"

def rejected_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = REJECTED
        item.save()
rejected_message.short_description = "Mark As Rejected"

def favorite_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = FAVORITED
        item.save()
favorite_message.short_description = "Mark As Favorite"

def pending_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = PENDING
        item.save()
pending_message.short_description = "Mark As Pending"

def legal_message(modeladmin, request, queryset):
    for item in queryset:
        item.status = LEGAL
        item.save()
legal_message.short_description = "Mark As Legal"


def admin_url(model, url, object_id=None):
    """
    Returns the URL for the given model and admin url name.
    """
    opts = model._meta
    url = "admin:%s_%s_%s" % (opts.app_label, opts.object_name.lower(), url)
    args = ()
    if object_id is not None:
        args = (object_id,)
    return reverse(url, args=args)

class SingletonAdmin(admin.ModelAdmin):
    """
    Admin class for models that should only contain a single instance
    in the database. Redirect all views to the change view when the
    instance exists, and to the add view when it doesn't.
    """

    def handle_save(self, request, response):
        """
        Handles redirect back to the dashboard when save is clicked
        (eg not save and continue editing), by checking for a redirect
        response, which only occurs if the form is valid.
        """
        form_valid = isinstance(response, HttpResponseRedirect)
        if request.POST.get("_save") and form_valid:
            return redirect("admin:index")
        return response

    def add_view(self, *args, **kwargs):
        """
        Redirect to the change view if the singleton instance exists.
        """
        try:
            singleton = self.model.objects.get()
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            kwargs.setdefault("extra_context", {})
            kwargs["extra_context"]["singleton"] = True
            response = super(SingletonAdmin, self).add_view(*args, **kwargs)
            return self.handle_save(args[0], response)
        return redirect(admin_url(self.model, "change", singleton.id))

    def changelist_view(self, *args, **kwargs):
        """
        Redirect to the add view if no records exist or the change
        view if the singleton instance exists.
        """
        try:
            singleton = self.model.objects.get()
        except self.model.MultipleObjectsReturned:
            return super(SingletonAdmin, self).changelist_view(*args, **kwargs)
        except self.model.DoesNotExist:
            return redirect(admin_url(self.model, "add"))
        return redirect(admin_url(self.model, "change", singleton.id))

    def change_view(self, *args, **kwargs):
        """
        If only the singleton instance exists, pass ``True`` for
        ``singleton`` into the template which will use CSS to hide
        the "save and add another" button.
        """
        kwargs.setdefault("extra_context", {})
        kwargs["extra_context"]["singleton"] = self.model.objects.count() == 1
        response = super(SingletonAdmin, self).change_view(*args, **kwargs)
        return self.handle_save(args[0], response)

class HideableAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if self.pref_model.objects.count():
            return super(HideableAdmin, self).get_model_perms(request)
        else:
            return {
                'add': False,
                'change': False,
                'delete': False,
            }

class MessageAdmin(admin.ModelAdmin):
    actions = [approve_message, rejected_message, favorite_message, pending_message, legal_message]
    list_display = ('id', 'admin_media_preview', 'message', 'status', 'media_type', 'network', 'date', 'tags', )
    list_filter = ('network', 'media_type', 'status', 'date', '_tags')
    list_display_links = ('id', 'admin_media_preview' )
    readonly_fields = ('admin_media_preview', 'reply_to',)
    exclude = ('tags', )
    ordering = ('-status', '-date')
    
    class Media:
        js = ("jquery.multiselect.js", "tag_multiselect.js", "json2.js", )
        css = { 'all': ("jquery.multiselect.css", ) }
        

class FacebookAccountAdmin(HideableAdmin):
    pref_model = FacebookSetting

class FacebookMessageAdmin(MessageAdmin, HideableAdmin):
    pref_model = FacebookSetting
    list_display = [c for c in MessageAdmin.list_display if c != 'tags']
    list_filter = [c for c in MessageAdmin.list_filter if c != '_tags']

class FacebookSearchAdmin(HideableAdmin):
    pref_model = FacebookSetting

class TwitterAccountAdmin(HideableAdmin):
    list_display = ('screen_name',)
    pref_model = TwitterSetting

    def add_view(self, request, form_url='', extra_context=None):
        log.debug("request: %s", request)
        log.debug("form_url: %s", form_url)
        log.debug("extra_context: %s", extra_context)
        return begin_auth(request)


class TwitterPublicAccountAdmin(HideableAdmin):
    pref_model = TwitterSetting

class TwitterMessageAdmin(MessageAdmin, HideableAdmin):
    pref_model = TwitterSetting
    list_display = ('id', 'admin_media_preview', 'message', 'status', 'media_type', 'date', )
    list_filter = ('twitter_search__search_term', 'twitter_account__screen_name', 'status', 'media_type', 'date')

class TwitterSearchAdmin(HideableAdmin):
    pref_model = TwitterSetting

class InstagramAccountAdmin(HideableAdmin):
    pref_model = InstagramSetting
    list_display = ('id', 'admin_image', 'username', 'name')
    list_filter = ('username', 'name')
    search_fields = ('username', 'name')

    def add_view(self, *args, **kwargs):
        if SOCIAL_INSTAGRAM_CLIENT_ID and SOCIAL_INSTAGRAM_REDIRECT_URI:
            params = urlencode({
                'client_id': SOCIAL_INSTAGRAM_CLIENT_ID,
                'redirect_uri': SOCIAL_INSTAGRAM_REDIRECT_URI,
                'response_type': 'code',
            })
            url = '?'.join(['https://api.instagram.com/oauth/authorize/', params])
            log.info('Login via Instagram API')
            log.info(url)
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(reverse('admin:social_instagramsetting_add'))


class InstagramPublicAccountAdmin(HideableAdmin):
    pref_model = InstagramSetting


class InstagramSearchAdmin(HideableAdmin):
    pref_model = InstagramSetting


class InstagramMessageAdmin(MessageAdmin, HideableAdmin):
    pref_model = InstagramSetting
    list_display = ('id', 'admin_image_low','message', 'status', 'media_type', 'date', )
    list_display_links = ('id', 'admin_image_low' )
    list_filter = ('status', 'media_type', 'date',)

class RSSAccountAdmin(HideableAdmin):
    pref_model = RSSSetting

class RSSMessageAdmin(HideableAdmin):
    pref_model = RSSSetting
    list_display = ('id', 'message', 'date')
    list_filter = ('rss_account__feed_name', 'status', 'media_type', 'date',)
