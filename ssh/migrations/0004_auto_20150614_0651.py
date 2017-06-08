# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0003_auto_20150613_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='server_ip',
            field=models.TextField(validators=[django.core.validators.RegexValidator(regex=b'^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$', message=b'Enter correct IP', code=b'invalid_key')]),
        ),
    ]
