# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_remove_instagramaccount_scrap_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsearch',
            name='filter_for_images',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instagramsearch',
            name='filter_for_videos',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
