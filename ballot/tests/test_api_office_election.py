from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest


class MeasureAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_office_election_with_id(self):
        resp = self.client.get(reverse('office_election_get',
                                       kwargs={'office_election_id': 1}))

        self.assertIn('id', resp.data)
        self.assertIn('office', resp.data)

    def test_candidate_with_id(self):
        resp = self.client.get(reverse('candidate_get',
                                       kwargs={'candidate_id': 1}))

        self.assertIn('id', resp.data)
        self.assertIn('first_name', resp.data)
        self.assertIn('last_name', resp.data)
        self.assertIn('party', resp.data)
