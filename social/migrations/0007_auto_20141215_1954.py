# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fix_scrap(apps, schema_editor):
    InstagramAccount = apps.get_model("social", "InstagramAccount")
    for ia in InstagramAccount.objects.all():
        ia.scrape_account = ia.scrap_account
        ia.save()


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_instagramaccount_scrape_profile'),
    ]

    operations = [
                  migrations.RunPython(fix_scrap)
    ]
