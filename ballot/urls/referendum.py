from django.conf.urls import patterns, url

from .. import views


urlpatterns = patterns(
    '',
    url(r'referendum/(?P<referendum_id>[0-9]+)$',
        views.ReferendumViewSet.as_view(actions={'get': 'retrieve'}),
        name='referendum_get'))
