# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0004_auto_20150614_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='ssh_key',
            field=models.TextField(verbose_name=b'Enter SSH Key', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9@=/+-.:;!_*\n\r ]*$', message=b'Key must be Alphanumeric!', code=b'invalid_key')]),
        ),
    ]
