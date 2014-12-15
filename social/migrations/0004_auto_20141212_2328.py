# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_twittersearch_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsearch',
            name='instagram_id',
            field=models.BigIntegerField(default=0, help_text=b'if not known, leave 0 and it will be looked up'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instagramsearch',
            name='username',
            field=models.CharField(help_text=b'If set, only this account will be searched', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
