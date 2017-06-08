from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	     url(r'^login/', 'loginsys.views.login'),
            url(r'^logout/', 'loginsys.views.logout'),
]
