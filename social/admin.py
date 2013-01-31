from django.contrib import admin
from .models import FacebookAccount, FacebookMessage


admin.site.register(FacebookAccount)
admin.site.register(FacebookMessage)