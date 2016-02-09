from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from ballot.models import Ballot
from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest


class BallotAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()
        cls.ballot = Ballot.objects.all()[0]

    def test_ballot(self):
        ballot_url = reverse('ballot_get', kwargs={'ballot_id': self.ballot.id})
        resp = self.client.get(ballot_url)

        self.assertIn('date', resp.data)
        self.assertIn('id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('ballot_items', resp.data)

        first_ballot_item = resp.data['ballot_items'][0]
        self.assertIn('id', first_ballot_item)
        self.assertIn('contest_type', first_ballot_item)
        self.assertIn('name', first_ballot_item)

    def test_current_ballot(self):
        ballot_url = reverse('current_ballot', kwargs={'locality_id': self.ballot.locality_id})
        resp = self.client.get(ballot_url)

        self.assertIn('date', resp.data)
        self.assertIn('id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('ballot_items', resp.data)

        first_ballot_item = resp.data['ballot_items'][0]
        self.assertIn('id', first_ballot_item)
        self.assertIn('contest_type', first_ballot_item)
        self.assertIn('name', first_ballot_item)
