from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class ContributorsAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_contributors(self):
        resp = self.client.get('/contributors/')
        self.assertTrue(len(resp.data) > 0)

        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('amount', row)
        self.assertIn('date', row)
