from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Candidate, OfficeElection
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
        Details for a single office election, including all candidates.
        """
        office_election = get_object_or_404(OfficeElection, id=office_election_id)
        return Response(OfficeElectionSerializer(office_election).data)


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
        Details for a single candidate.
        """
        candidate = get_object_or_404(Candidate, id=candidate_id)
        return Response(CandidateSerializer(candidate).data)
