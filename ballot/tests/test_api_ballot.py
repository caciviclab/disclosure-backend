from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from ballot.models import Ballot
from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest


class BallotAPITest(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()
        cls.ballot = Ballot.objects.all()[0]

    def test_ballot(self):
        ballot_url = reverse(
            'ballot_get', kwargs={'ballot_id': self.ballot.id})
        resp = self.client.get(ballot_url)

        self.assertEqual(self.ballot.id, resp.data['id'])
        self.assertEqual(self.ballot.date, resp.data['date'])
        self.assertEqual(self.ballot.locality.id, resp.data['locality_id'])
        self.assertIn('ballot_items', resp.data)

        # TO DO: validate the values of the ballot item
        first_ballot_item = resp.data['ballot_items'][0]
        self.assertIn('id', first_ballot_item)
        self.assertIn('contest_type', first_ballot_item)
        self.assertIn('name', first_ballot_item)

    def test_ballot_bad_id_404(self):
        """ Unknown ballot ID"""
        ballot_url = reverse(
            'ballot_get', kwargs={'ballot_id': 0})
        resp = self.client.get(ballot_url)

        self.assertEqual(resp.status_code, 404, ballot_url)

    def test_current_ballot(self):
        ballot_url = reverse(
            'current_ballot', kwargs={'locality_id': self.ballot.locality_id})
        resp = self.client.get(ballot_url)

        self.assertEqual(self.ballot.id, resp.data['id'])
        self.assertEqual(self.ballot.date, resp.data['date'])
        self.assertEqual(self.ballot.locality.id, resp.data['locality_id'])
        self.assertIn('ballot_items', resp.data)

        # TO DO: validate the values of the ballot item
        first_ballot_item = resp.data['ballot_items'][0]
        self.assertIn('id', first_ballot_item)
        self.assertIn('contest_type', first_ballot_item)
        self.assertIn('name', first_ballot_item)
