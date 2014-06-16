from django.contrib import admin

from ..models import (FacebookAccount, FacebookMessage, FacebookSearch,
                      TwitterAccount, TwitterMessage, TwitterSearch,
                      RSSAccount, RSSMessage, Message,
                      InstagramAccount, InstagramSearch, InstagramMessage,
                      TwitterSetting, FacebookSetting, InstagramSetting,
                      FacebookPublicAccount, TwitterPublicAccount, InstagramPublicAccount,
                      RSSSetting)
from .models import (SingletonAdmin, MessageAdmin, FacebookAccountAdmin, FacebookSearchAdmin,
                     FacebookMessageAdmin, TwitterAccountAdmin, TwitterPublicAccountAdmin,
                     TwitterMessageAdmin, TwitterSearchAdmin,
                     InstagramAccountAdmin, InstagramPublicAccountAdmin, InstagramSearchAdmin,
                     InstagramMessageAdmin, RSSAccountAdmin, RSSMessageAdmin,)


admin.site.register(Message, MessageAdmin)

admin.site.register(FacebookSetting, SingletonAdmin)
admin.site.register(FacebookAccount, FacebookAccountAdmin)
admin.site.register(FacebookPublicAccount, FacebookAccountAdmin)
admin.site.register(FacebookMessage, FacebookMessageAdmin)
admin.site.register(FacebookSearch,  FacebookSearchAdmin)

admin.site.register(TwitterSetting, SingletonAdmin)
admin.site.register(TwitterAccount, TwitterAccountAdmin)
admin.site.register(TwitterPublicAccount, TwitterPublicAccountAdmin)
admin.site.register(TwitterMessage, TwitterMessageAdmin)
admin.site.register(TwitterSearch, TwitterSearchAdmin)

admin.site.register(InstagramSetting, SingletonAdmin)
admin.site.register(InstagramAccount, InstagramAccountAdmin)
admin.site.register(InstagramPublicAccount, InstagramPublicAccountAdmin)
admin.site.register(InstagramSearch, InstagramSearchAdmin)
admin.site.register(InstagramMessage, InstagramMessageAdmin)

admin.site.register(RSSSetting, SingletonAdmin)
admin.site.register(RSSAccount, RSSAccountAdmin)
admin.site.register(RSSMessage, RSSMessageAdmin)
