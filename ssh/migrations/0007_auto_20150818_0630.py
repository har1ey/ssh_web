# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0006_auto_20150625_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='date_action',
            field=models.DateTimeField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='key',
            name='ssh_key',
            field=models.TextField(verbose_name=b"Enter SSH Key (Syntax: 'type key comment', Example: 'ssh-rsa key test_comment')"),
        ),
    ]
