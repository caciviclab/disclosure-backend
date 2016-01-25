from django.core.urlresolvers import reverse
from django.db.models import Q
from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest
from locality.models import City


class ContributorsAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_contributors(self):
        # Get first city with non-None name
        city = City.objects.filter(~Q(name=None))[0]

        contributors_url = reverse('locality_contributors',
                                   kwargs={'locality_id': city.id})
        resp = self.client.get(contributors_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('amount', row)
        self.assertIn('date', row)
