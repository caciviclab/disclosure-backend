from django.core.urlresolvers import reverse
from django.db.models import Q
from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest
from ballot.models import Candidate, Referendum


class OpposingTests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass(test_agency='COS', test_year='2015')
        APITestCase.setUpClass()

    def test_candidate_opposing_list(self):
        candidate = Candidate.objects.filter(~Q(last_name=None))[0]
        opposing_url = reverse('candidate_opposing',
                               kwargs={'candidate_id': candidate.id})
        resp = self.client.get(opposing_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions', row)

    def test_candidate_supporting_list(self):
        candidate = Candidate.objects.filter(~Q(last_name=None))[0]
        supporting_url = reverse('candidate_supporting',
                                 kwargs={'candidate_id': candidate.id})
        resp = self.client.get(supporting_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions', row)

    def test_referendum_opposing_list(self):
        referendum = Referendum.objects.all()[0]
        opposing_url = reverse('referendum_opposing',
                               kwargs={'referendum_id': referendum.id})
        resp = self.client.get(opposing_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions', row)

    def test_referendum_supporting_list(self):
        referendum = Referendum.objects.all()[0]
        supporting_url = reverse('referendum_supporting',
                                 kwargs={'referendum_id': referendum.id})
        resp = self.client.get(supporting_url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions', row)
