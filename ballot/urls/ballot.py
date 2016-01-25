from django.conf.urls import patterns, url
from django.contrib import admin

from ..views import ballot as views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^locality/(?P<locality_id>[0-9]+)/ballot/$', views.ballot_view,
        name='locality_ballot'))
