from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from finance.tests.utils import with_form460A_data
from finance.models import Beneficiary


@with_form460A_data(test_agency='COS', test_year='2015')
class OpposingTests(APITestCase):

    def do_the_thing_for_candidates(self, support):
        beneficiary = Beneficiary.objects.filter(
            ballot_item_selection__ballot_item__contest_type='O')[0]
        beneficiary.support = support
        beneficiary.save()
        candidate = beneficiary.ballot_item_selection.reverse_lookup()

        url = reverse('candidate_%s' % ('supporting' if support else 'opposing'),
                      kwargs={'candidate_id': candidate.id})
        resp = self.client.get(url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)

    def test_candidate_opposing_list(self):
        return self.do_the_thing_for_candidates(support=False)

    def test_candidate_supporting_list(self):
        return self.do_the_thing_for_candidates(support=True)

    def do_the_thing_for_referendums(self, support):
        beneficiary = Beneficiary.objects.filter(
            ballot_item_selection__ballot_item__contest_type='R')[0]
        beneficiary.support = support
        beneficiary.save()

        referendum = beneficiary.ballot_item_selection.ballot_item.reverse_lookup()
        url = reverse('referendum_%s' % ('supporting' if support else 'opposing'),
                      kwargs={'referendum_id': referendum.id})
        resp = self.client.get(url)
        self.assertTrue(len(resp.data) > 0)

        # TODO: replace dummy tests with live data tests.
        row = resp.data[0]
        self.assertIn('name', row)
        self.assertIn('contributions_received', row)

    def test_referendum_opposing_list(self):
        return self.do_the_thing_for_referendums(support=False)

    def test_referendum_supporting_list(self):
        return self.do_the_thing_for_referendums(support=True)
