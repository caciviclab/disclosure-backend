from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from ballot.models import Ballot
from finance.models import IndependentMoney
from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest
from locality.models import City


class LocationTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_disclosure_summary_contains_data(self):
        # Get first city with non-None name
        city = City.objects.get(name='Murrieta')
        ballot = Ballot.objects.filter(locality_id=city.id)[0]
        supporting_url = reverse('locality_disclosure_summary',
                                 kwargs={'ballot_id': ballot.id})
        resp = self.client.get(supporting_url)
        self.assertEqual(resp.status_code, 200, supporting_url)

        data = resp.data
        self.assertEqual(data['contribution_count'],
                         IndependentMoney.objects.all().count())

        self.assertEqual(data['location']['name'], city.name)
        self.assertEqual(data['location']['id'], city.id)

        self.assertIn('contribution_by_type', data)
        self.assertIn('contribution_by_area', data)

    def test_disclosure_summary_no_data_404(self):
        # Get first city with non-None name
        city = City.objects.get(name='Anaheim')
        ballot, _ = Ballot.objects.get_or_create(locality_id=city.id)
        supporting_url = reverse('locality_disclosure_summary',
                                 kwargs={'ballot_id': ballot.id})
        resp = self.client.get(supporting_url)
        self.assertEqual(resp.status_code, 200, supporting_url)

    def test_disclosure_summary_bad_id_404(self):
        """ Unknown locality ID"""
        supporting_url = reverse('locality_disclosure_summary',
                                 kwargs={'ballot_id': 0})
        resp = self.client.get(supporting_url)
        self.assertEqual(resp.status_code, 404, supporting_url)
