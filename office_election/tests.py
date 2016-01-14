from django.test import TestCase

from office_election.models import Candidate, OfficeElection, Office
from ballot.models import Ballot
from locality.models import City, State


class OfficeElectionTest(TestCase):
    def test_create_candidate(self):
        """
        Candidates have extra logic in their initializer. Play with it.
        """
        state, _ = State.objects.get_or_create(name='California')
        city, _ = City.objects.get_or_create(name='San Diego', state=state)
        office, _ = Office.objects.get_or_create(name='Mayor', locality=city)
        ballot, _ = Ballot.objects.get_or_create(locality=city)
        kwargs = dict(first_name='Ben', last_name='Cip')

        # Set via office_election
        office_election, _ = OfficeElection.objects.get_or_create(
            office=office, ballot=ballot)
        cand = Candidate(office_election=office_election, **kwargs)
        self.assertEqual(cand.office_election.id, cand.ballot_item.id,
                         'office_election and ballot_item should match.')
        cand.save()  # smoke test
        Candidate.objects.all().delete()

        # Set via ballot_item
        office_election, _ = OfficeElection.objects.get_or_create(
            office=office, ballot=ballot)
        cand = Candidate(ballot_item=office_election, **kwargs)
        self.assertEqual(cand.office_election.id, cand.ballot_item.id,
                         'office_election and ballot_item should match.')

        # Load
        cand.save()
        cand = Candidate.objects.all()[0]
        self.assertEqual(cand.office_election.id, cand.ballot_item.id,
                         'office_election and ballot_item should match.')
