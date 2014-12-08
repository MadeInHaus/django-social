# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookaccount',
            name='last_poll_time',
            field=models.IntegerField(default=1418081661),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebookpublicaccount',
            name='last_poll_time',
            field=models.IntegerField(default=1418081661),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksearch',
            name='last_poll_time',
            field=models.IntegerField(default=1418081661),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersearch',
            name='search_until',
            field=models.IntegerField(default=1418081661),
            preserve_default=True,
        ),
    ]
