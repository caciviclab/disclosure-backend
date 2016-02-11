from django.test import TestCase

from ballot.models import Ballot, Referendum, ReferendumSelection
from locality.models import City, State


class ObjectCreateTest(TestCase):
    def test_create_empty(self):
        referendum = Referendum()  # noqa
        referendum_selection = ReferendumSelection()  # noqa


class ReferendumTest(TestCase):
    def test_create_candidate(self):
        """
        Candidates have extra logic in their initializer. Play with it.
        """
        state, _ = State.objects.get_or_create(name='California')
        city, _ = City.objects.get_or_create(name='San Diego', state=state)
        ballot, _ = Ballot.objects.get_or_create(locality=city)
        referendum, _ = Referendum.objects.get_or_create(
            ballot=ballot, title='Ref1', number='BB')
        selection, _ = ReferendumSelection.objects.get_or_create(
            ballot_item=referendum, in_favor=True)

        # Smoke test to string
        self.assertNotIn('Referendum', str(referendum))
        self.assertNotIn('ReferendumSelection', str(selection))
