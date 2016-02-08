from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from finance.models import IndependentMoney

from finance.tests.test_command import WithForm460ADataTest


class ContributorsAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

        money = IndependentMoney.objects.all()[0]
        cls.beneficiary = money.beneficiary

    def test_contributors(self):
        contributors_url = reverse('contributors_list',
                                   kwargs={'committee_id': self.beneficiary.id})
        resp = self.client.get(contributors_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertTrue('expenditures' in row or 'contributions' in row)
        self.assertIn('type', row)

    def test_contributors_summary(self):
        committee_url = reverse('contributors_summary',
                                kwargs={'committee_id': self.beneficiary.id})
        resp = self.client.get(committee_url)

        # TODO: replace dummy tests with live data tests.
        self.assertIn('contribution_by_type', resp.data)
        self.assertIn('contribution_by_area', resp.data)
