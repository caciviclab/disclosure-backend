from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class BallotAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_ballot_endpoint(self):
        resp = self.client.get('/ballot/')

        self.assertIn('ballot_id', resp.data)
        self.assertIn('locality_id', resp.data)
        self.assertIn('contests', resp.data)
