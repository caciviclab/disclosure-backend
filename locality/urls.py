from django.conf.urls import patterns, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Details for specific objects
    url(r'^locality/(?P<locality_id>[0-9]+)$',
        views.LocalityViewSet.as_view(actions={'get': 'retrieve'}),
        name='locality_get'))
