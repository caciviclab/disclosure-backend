from django.core.urlresolvers import reverse
from django.db.models import Q
from rest_framework.test import APITestCase

from finance.models import Committee
from finance.tests.test_command import WithForm460ADataTest


class CommitteeAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_committee_with_id(self):
        # Get first committee with non-None name
        committee = Committee.objects.filter(~Q(name=None))[0]

        committee_url = reverse('committee_get', kwargs={'committee_id': committee.id})
        resp = self.client.get(committee_url)

        # TODO: replace dummy tests with live data tests.
        self.assertIn('filer_id', resp.data)
        self.assertIn('name', resp.data)
