from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
                       url(r'^ssh/select/all/$', 'ssh.views.all'),
                       url(r'^ssh/select/(?P<server_id>\d+)/$', 'ssh.views.select'),
                       url(r'^ssh/info/(?P<key_id>\d+)/$', 'ssh.views.get_info'),
                       url(r'^ssh/key/$', 'ssh.views.key'),
                       url(r'^ssh/key/clear/$', 'ssh.views.clear_info'),
                       url(r'^add/$', 'ssh.views.add_key'),
                       url(r'^del/$', 'ssh.views.del_key'),
                       url(r'^check/$', 'ssh.views.check_key'),
                       url(r'^last/$', 'ssh.views.last_k'),
                       url(r'^auth/', include('loginsys.urls')),
                       url(r'^', 'ssh.views.page'),
]

