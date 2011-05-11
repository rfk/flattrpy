from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'flattrpy.web.views.index', ),
    url(r'^oauth_callback/$', 'flattrpy.web.views.oauth_callback', ),
    url(r'^flattrit/$', 'flattrpy.web.views.flattrit', ),
)
