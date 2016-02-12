from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest


class BallotAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_ballot(self):
        ballot_url = reverse('ballot_get', kwargs={'ballot_id': 1})
        resp = self.client.get(ballot_url)

        self.assertIn('date', resp.data)
        self.assertIn('id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('ballot_items', resp.data)

    def test_current_ballot(self):
        ballot_url = reverse('current_ballot', kwargs={'locality_id': 1})
        resp = self.client.get(ballot_url)

        self.assertIn('date', resp.data)
        self.assertIn('id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('ballot_items', resp.data)
