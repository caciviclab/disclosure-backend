from django.test import TestCase

from election_day.models import ElectionDay
from election_day.views import ElectionDayView
from locality.models import City, State
from ballot.models import Ballot, Office


class ElectionDayTest(TestCase):
    def test_election_day_view(self):
        """
        Add election_day, output it.
        """
        state, _ = State.objects.get_or_create(name='California')
        city, _ = City.objects.get_or_create(name='San Diego', state=state)
        office, _ = Office.objects.get_or_create(name='Mayor', locality=city)
        ballot, _ = Ballot.objects.get_or_create(locality=city)
        election_day, _ = ElectionDay.objects.get_or_create(ballot=ballot)

        # Smoke test
        ElectionDayView().list(request=None)
