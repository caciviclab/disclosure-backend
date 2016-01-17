from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class CommitteeAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_committee_with_id(self):
        resp = self.client.get('/committee/%d' % 1)

        self.assertIn('committee_id', resp.data)
        self.assertIn('name', resp.data)
        self.assertIn('contribution_by_type', resp.data)
        self.assertIn('contribution_by_area', resp.data)
