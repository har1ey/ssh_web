# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0002_auto_20150612_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='server_ip',
            field=models.TextField(validators=[django.core.validators.RegexValidator(regex=b'((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)', message=b'rrfrr', code=b'invalid_key')]),
        ),
    ]
