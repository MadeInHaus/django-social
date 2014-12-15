# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20141215_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramaccount',
            name='scrap_profile',
        ),
    ]
