# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0008_auto_20150818_0653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='key',
            name='date_action',
        ),
    ]
