from django.core.urlresolvers import reverse
from django.db.models import Q
from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest
from locality.models import City
from finance.models import IndependentMoney


class LocationTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_list_contains_data(self):
        # Get first city with non-None name
        city = City.objects.filter(~Q(name=None))[0]

        supporting_url = reverse('locality_detail',
                                 kwargs={'locality_id': city.id})
        resp = self.client.get(supporting_url)
        data = resp.data
        self.assertEqual(data['contribution_count'],
                         IndependentMoney.objects.all().count())

        self.assertEqual(data['location']['name'], city.name)
        self.assertEqual(data['location']['id'], city.id)

        self.assertIn('contribution_by_type', data)
        self.assertIn('contribution_by_area', data)
