from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns=patterns('',
                     url(r'^player/(?P<player_id>\w+)/$', 'honbot.views.playerShow'),
                     url('', 'honbot.views.home'),
                     )

