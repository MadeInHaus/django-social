# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_twittersearch_filter_for_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='twittersearch',
            name='account',
            field=models.CharField(default=b'', help_text=b'Account handle to search, leave blank to search all users', max_length=30),
            preserve_default=True,
        ),
    ]
