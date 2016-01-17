from django.db.models import Q
from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest
from locality.models import City


class SearchTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_search_city(self):
        # Get first city with non-None name
        city = City.objects.filter(~Q(name=None))[0]

        resp = self.client.get('/search/?q=' + city.name)
        self.assertEqual(len(resp.data), 1)
        row = resp.data[0]
        self.assertIn('id', row)
        self.assertEqual(row['name'], city.name)
        self.assertEqual(row['id'], city.id)
