from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views as static_views

import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', static_views.serve),
)
