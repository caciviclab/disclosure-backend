from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.utils import with_form460A_data
from ballot.models import Candidate, OfficeElection


@with_form460A_data
class OfficeElectionAPITest(APITestCase):

    def test_office_election_with_id(self):
        office_election = OfficeElection.objects.all()[0]
        resp = self.client.get(
            reverse('office_election_get',
                    kwargs={'office_election_id': office_election.id}))

        self.assertEqual(office_election.id, resp.data['id'])
        self.assertEqual(office_election.office.id, resp.data['office'])
        self.assertEqual(office_election.ballot.id, resp.data['ballot_id'])
        self.assertNotIn('contest_type', resp.data)

    def test_office_election_bad_id_404(self):
        """ Unknown office election ID"""
        resp = self.client.get(
            reverse('office_election_get', kwargs={'office_election_id': 0}))

        self.assertEqual(resp.status_code, 404)


@with_form460A_data
class CandidateAPITest(APITestCase):

    def test_candidate_with_id(self):
        candidate = Candidate.objects.all()[0]
        resp = self.client.get(
            reverse('candidate_get',
                    kwargs={'candidate_id': candidate.id}))

        self.assertEqual(candidate.id, resp.data['id'])
        self.assertEqual(candidate.first_name, resp.data['first_name'])
        self.assertEqual(candidate.last_name, resp.data['last_name'])
        self.assertEqual(candidate.party, resp.data['party'])

    def test_candidate_bad_id_404(self):
        """ Unknown candidate ID"""
        resp = self.client.get(
            reverse('candidate_get', kwargs={'candidate_id': 0}))

        self.assertEqual(resp.status_code, 404)
