# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_auto_20141215_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittermessage',
            name='in_reply_to_screen_name',
            field=models.CharField(max_length=400, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittermessage',
            name='in_reply_to_status_id',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittermessage',
            name='in_reply_to_user_id',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersearch',
            name='account',
            field=models.CharField(help_text=b'Account handle to search, leave blank to search all users', max_length=30, blank=True, default=b''),
            preserve_default=True,
        ),
    ]
