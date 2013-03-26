# project wide urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

# import your urls from each app here, as needed
import honbot.urls

handler404 = 'honbot.views.v404'

urlpatterns = patterns('',
    url('', include(honbot.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
