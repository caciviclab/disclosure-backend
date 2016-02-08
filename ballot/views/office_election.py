from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ..serializers import OfficeElectionSerializer, CandidateSerializer  # noqa


class OfficeElectionViewSet(viewsets.ViewSet):
    """
    Contest for an office in a specific locality.
    ---

    retrieve:
      response_serializer: OfficeElectionSerializer
    """

    @detail_route(['GET'])
    def retrieve(self, request, office_election_id):
        """
        Office Election text / details
        """
        return Response({
            'id': int(office_election_id),
            'office': 'Mayor',
            'candidates': [
                {
                    'id': 1,
                    'first_name': 'Cand',
                    'last_name': 'One'
                },
                {
                    'id': 2,
                    'first_name': 'Other',
                    'last_name': 'Cand'
                }
            ]
        })


class CandidateViewSet(viewsets.ViewSet):
    """
    Candidate for an office in a specific locality.
    ---

    retrieve:
      response_serializer: CandidateSerializer
    """

    @detail_route(['GET'])
    def retrieve(self, request, candidate_id):
        """
        Candidate text / details
        """
        return Response({
            'id': int(candidate_id),
            'first_name': 'Ben',
            'middle_name': '',
            'last_name': 'Cip',
            'party': None,
        })
