from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from finance.models import IndependentMoney
from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest


class ContributionsAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

        for m in IndependentMoney.objects.all():
            if hasattr(m.benefactor, 'committeebenefactor'):
                cls.committee = m.benefactor.committeebenefactor
                break

    def test_contributions_with_id(self):

        committee_url = reverse('contributions_list', kwargs={'committee_id': self.committee.id})
        resp = self.client.get(committee_url)
        self.assertIn('amount', resp.data[0], resp.data)
