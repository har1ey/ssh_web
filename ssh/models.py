from django.db import models
from django.core.validators import RegexValidator


class Server(models.Model):
    class Meta:
        db_table = "Servers"

    server_ip = models.TextField(validators=[
        RegexValidator(
            regex='^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
            message='Enter correct IP',
            code='invalid_key'
        ),
    ])
    server_login = models.TextField()
    server_pass = models.TextField(blank=True)
    server_comment = models.TextField()
    server_select = models.BooleanField(default=False)


class Key(models.Model):
    class Meta:
        db_table = "Keys"

    ssh_key = models.TextField(verbose_name="Enter SSH Key (Syntax: 'type key comment', Example: 'ssh-rsa key test_comment')",
                               )
    key_action = models.TextField()