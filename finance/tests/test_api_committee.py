from django.core.urlresolvers import reverse
from django.db.models import Q
from rest_framework.test import APITestCase

from finance.models import Committee
from finance.tests.utils import with_form460A_data


@with_form460A_data
class CommitteeAPITests(APITestCase):

    def test_committee_with_id(self):
        # Get first committee with non-None name
        committee = Committee.objects.filter(~Q(name=None))[0]

        committee_url = reverse('committee_get', kwargs={'committee_id': committee.id})
        resp = self.client.get(committee_url)

        # TODO: replace dummy tests with live data tests.
        self.assertIn('filer_id', resp.data)
        self.assertIn('name', resp.data)
