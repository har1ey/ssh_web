# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0007_auto_20150818_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='date_action',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
