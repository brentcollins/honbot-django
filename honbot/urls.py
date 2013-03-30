# app specific urls
from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url('^$', 'honbot.views.home'),
    url(r'^player/(?P<name>.*)/$', 'honbot.views.players'),
    url(r'^match/(?P<match_id>\d+)/$', 'honbot.views.match_view'),
    url(r'^chat/(?P<match_id>\d+)/$', 'honbot.views.chat_view'),
)
