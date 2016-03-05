from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest
from ballot.models import Ballot, Referendum


class ReferendumAPITest(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_referendum_with_id(self):
        # referendum = Referendum.objects.all()[0]
        ballot = Ballot.objects.all()[0]
        referendum, _ = Referendum.objects.get_or_create(
            ballot=ballot, title='dummy', number='r123')

        resp = self.client.get(
            reverse('referendum_get',
                    kwargs={'referendum_id': referendum.id}))

        self.assertEqual(referendum.id, resp.data['id'])
        self.assertEqual(referendum.title, resp.data['title'])
        self.assertEqual(referendum.number, resp.data['number'])
        self.assertEqual(referendum.ballot.id, resp.data['ballot_id'])
        self.assertNotIn('ballot', resp.data)

    def test_referendum_bad_id_404(self):
        """ Unknown referendum ID"""
        resp = self.client.get(
            reverse('referendum_get', kwargs={'referendum_id': 0}))

        self.assertEqual(resp.status_code, 404)
