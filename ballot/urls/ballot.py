from django.conf.urls import patterns, url

from .. import views


urlpatterns = patterns(
    '',
    url(r'ballot/(?P<ballot_id>[0-9]+)$',
        views.BallotViewSet.as_view(actions={'get': 'retrieve'}),
        name="ballot_get"),
    url(r'locality/(?P<locality_id>[0-9]+)/current_ballot$',
        views.CurrentBallotViewSet.as_view(actions={'get': 'current_ballot'}),
        name="current_ballot"))
