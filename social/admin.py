from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import FacebookAccount, FacebookMessage, TwitterAccount, TwitterMessage,\
                    TwitterSearch, RSSAccount, RSSMessage, Message, InstagramSearch, InstagramMessage, \
                    TwitterSetting, FacebookSetting, InstagramSetting, RSSSetting, APPROVED, PENDING, FAVORITED, REJECTED
from .views import begin_auth

from logging import getLogger

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

class MessageAdmin(admin.ModelAdmin):
    actions = [approve_message, rejected_message, favorite_message, pending_message]
    list_display = ('id','message', 'status', 'network')
    list_filter = ('network', 'status')

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)

    def add_view(self, request, form_url='', extra_context=None):
        log.debug("request: %s", request)
        log.debug("form_url: %s", form_url)
        log.debug("extra_context: %s", extra_context)
        return begin_auth(request)

class TwitterMessageAdmin(MessageAdmin):
    list_display = ('id','message', 'status')
    list_filter = ('twitter_search__search_term', 'twitter_account__screen_name', 'status')


class InstagramMessageAdmin(MessageAdmin):
    list_display = ('id','admin_image_low','message', 'status')
    list_filter = ('status', )


admin.site.register(TwitterSetting, SingletonAdmin)
admin.site.register(FacebookSetting, SingletonAdmin)
admin.site.register(InstagramSetting, SingletonAdmin)
admin.site.register(RSSSetting, SingletonAdmin)

admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage, MessageAdmin)
admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterMessage, TwitterMessageAdmin)
admin.site.register(TwitterSearch)
admin.site.register(InstagramSearch)
admin.site.register(InstagramMessage, InstagramMessageAdmin)
admin.site.register(Message, MessageAdmin)



class RSSMessageAdmin(admin.ModelAdmin):
    list_display = ('id','message')
    list_filter = ('rss_account__feed_name', 'status')

admin.site.register(RSSAccount)
admin.site.register(RSSMessage, RSSMessageAdmin)
