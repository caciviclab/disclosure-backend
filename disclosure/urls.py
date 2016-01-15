from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from rest_framework.routers import SimpleRouter

import election_day.views
from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.homepage_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True}),
    url(r'^search/', views.search_view),
    url(r'^locations/(?P<fips_id>[0-9]+)$', views.location_view),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'', include('locality.urls')),
)

# Register all API Viewsets:
api = SimpleRouter()
api.register(r'contributions', views.Contribution)
api.register(r'elections', election_day.views.ElectionDay)
urlpatterns += api.urls
