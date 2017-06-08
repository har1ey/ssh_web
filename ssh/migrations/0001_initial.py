# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ssh_key', models.TextField(verbose_name=b'Enter SSH Key', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z0-9@=/+-.:;!_\n\r ]*$', message=b'Key must be Alphanumeric!', code=b'invalid_key')])),
                ('key_action', models.TextField()),
            ],
            options={
                'db_table': 'Keys',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_ip', models.TextField()),
                ('server_login', models.TextField()),
                ('server_pass', models.TextField()),
                ('server_comment', models.TextField()),
                ('server_select', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Servers',
            },
        ),
    ]
