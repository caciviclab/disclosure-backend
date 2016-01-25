from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class BallotAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_ballot_endpoint(self):
        ballot_url = reverse('locality_ballot', kwargs={'locality_id': 1})
        resp = self.client.get(ballot_url)

        self.assertIn('ballot_id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('contests', resp.data)
