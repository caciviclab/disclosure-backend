from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Ballot
from ..serializers import BallotSerializer  # noqa


class BallotViewSet(viewsets.ViewSet):
    """
    Any ballot, containing all ballot items.
    ---
    retrieve:
      response_serializer: BallotSerializer
    """
    @detail_route(['GET'])
    def retrieve(self, request, ballot_id, locality_id=None):
        """
        Ballot data, including a list of ballot items.
        """
        ballot = get_object_or_404(Ballot, id=ballot_id)
        return Response(BallotSerializer(ballot).data)


class CurrentBallotViewSet(BallotViewSet):
    """
    Current ballot, containing all ballot items.
    ---

    current_ballot:
      response_serializer: BallotSerializer
    """

    @detail_route(['GET'])
    def current_ballot(self, request, locality_id):
        """
        The most recent active ballot.
        """
        return super(CurrentBallotViewSet, self).retrieve(
            request=request, ballot_id=1, locality_id=locality_id)
