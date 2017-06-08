# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0005_auto_20150624_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='ssh_key',
            field=models.TextField(verbose_name=b"Enter SSH Key (Syntax: 'type key comment')", validators=[django.core.validators.RegexValidator(regex=b'^(ssh-rsa|ssh-dss|pgp-sign-rsa|pgp-sign-dss)\\s[a-zA-Z0-9@=/+-.:;!_\n]+\\s.+', message=b'Enter correct syntax', code=b'invalid_key')]),
        ),
    ]
