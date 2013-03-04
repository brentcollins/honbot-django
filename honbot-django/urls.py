# project wide urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# import your urls from each app here, as needed
import honbot.urls

urlpatterns = patterns('',
    # urls specific to this app
    url('^$', include(honbot.urls)),
    url(r'^player/(?P<name>\w+)/$', 'honbot.views.players'),
    (r'^favicon.ico$', 'django.views.static.serve', {'document_root': '/path/to/favicon'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),


)
