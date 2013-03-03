# app specific urls
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url('^$', 'honbot.views.home'),
    url('^player/(?P<string>[-\w]+)', 'honbot.views.home'),
)
