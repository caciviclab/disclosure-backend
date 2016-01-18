from rest_framework.test import APITestCase

from .test_command import WithForm460ADataTest
from finance.models import IndependentMoney


class IndependentMoneyTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        APITestCase.setUpClass()
        WithForm460ADataTest.setUpClass()

    def test_list_contains_data(self):
        resp = self.client.get('/contributions/')
        self.assertGreater(len(resp.data), 0)
        row = resp.data[0]
        self.assertIn('amount', row, row)

    def test_retrieve_contains_data(self):
        first_contribution_id = IndependentMoney.objects.all()[0].id
        resp = self.client.get(
            '/contributions/{0}/'.format(first_contribution_id))
        self.assertIn('amount', resp.data, resp.data)
