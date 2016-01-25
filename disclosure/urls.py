from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.homepage_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True}),

    url(r'', include('ballot.urls')),
    url(r'', include('election_day.urls')),
    url(r'', include('finance.urls')),
    # url(r'', include('locality.urls')),  # empty
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^search/', views.search_view,
        name='search'),

    # Details for specific objects
    url(r'^locations/(?P<locality_id>[0-9]+)$', views.location_view,
        name='locality_detail'),
    url(r'^committee/(?P<committee_id>[0-9]+)$', views.committee_view,
        name='committee_detail'),

    # Funding queries for a specific locality.
    url(r'^locality/(?P<locality_id>[0-9]+)/contributors/$',
        views.contributor_view,
        name='locality_contributors'),
    url(r'^locality/(?P<locality_id>[0-9]+)/supporting/$',
        views.supporting_view,
        name='locality_supporting'),
    url(r'^locality/(?P<locality_id>[0-9]+)/opposing/$',
        views.opposing_view,
        name='locality_opposing'))
