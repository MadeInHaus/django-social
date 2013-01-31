from django.contrib import admin
from .models import FacebookAccount, FacebookMessage, TwitterAccount, TwitterMessage


admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage)

class TwitterProfileAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)
    

admin.site.register(TwitterAccount, TwitterProfileAdmin)
admin.site.register(TwitterMessage)
