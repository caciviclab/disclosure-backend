from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest
from locality.models import City


class SearchTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_search_city_with_data(self):
        # Get first city with non-None name
        city = City.objects.get(name='Murrieta')

        search_url = '%s?q=%s' % (reverse('search'), city.name)
        resp = self.client.get(search_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

        row = resp.data[0]
        self.assertIn('id', row)
        self.assertEqual(row['name'], city.name)
        self.assertEqual(row['id'], city.id)

    def test_search_city_no_data(self):
        # Get first city with non-None name
        city = City.objects.get(name='Anaheim')

        search_url = '%s?q=%s' % (reverse('search'), city.name)
        resp = self.client.get(search_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 0)
