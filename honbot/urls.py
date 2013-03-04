# app specific urls
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url('^$', 'honbot.views.home'),
)
