from django.conf.urls import patterns, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^measure/(?P<measure_id>[0-9]+)$', views.measure_view),
    url(r'^ballot/$', views.ballot_view))
