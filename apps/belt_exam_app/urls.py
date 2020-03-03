from django.conf.urls import url
from . import views
#from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^wishes$', views.wishes),
    url(r'^wishes/new$', views.wishes_new),
    url(r'^wishes/create$', views.wishes_create),
    url(r'^wishes/remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.edit_page),
    url(r'^wishes/edit/process/(?P<id_wish_to_edit>\d+)$', views.edit_process),
    url(r'^wishes/granted/(?P<wish_id>\d+)$', views.granted),
    url(r'^wishes/(?P<wish_id>\d+)/likes$', views.likes),
    url(r'^wishes/stats$', views.stats),
]