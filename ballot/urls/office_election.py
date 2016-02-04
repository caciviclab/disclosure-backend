from django.conf.urls import patterns, url

from .. import views


urlpatterns = patterns(
    '',
    url(r'office_election/(?P<office_election_id>[0-9]+)$',
        views.OfficeElectionViewSet.as_view(actions={'get': 'retrieve'}),
        name='office_election_get'),
    url(r'candidate/(?P<candidate_id>[0-9]+)$',
        views.CandidateViewSet.as_view(actions={'get': 'retrieve'}),
        name='candidate_get'))
