from django.contrib import admin
from ssh.models import Server
from django.contrib.auth.models import *
# Register your models here.

class ExtendAdmin(admin.ModelAdmin):
    #fields = ['ssh']
    list_display = ('server_ip', 'server_comment',)
    search_fields = ['server_ip']

admin.site.register(Server, ExtendAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)