# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_instagramsearch_last_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramaccount',
            name='scrape_profile',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
