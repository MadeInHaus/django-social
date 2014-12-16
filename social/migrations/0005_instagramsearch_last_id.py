# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20141212_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsearch',
            name='last_id',
            field=models.CharField(help_text=b'greatest id seen so far for this search,  searches will search from this id forward', max_length=42, null=True, blank=True),
            preserve_default=True,
        ),
    ]
