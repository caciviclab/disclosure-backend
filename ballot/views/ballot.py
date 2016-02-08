from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from ..models import Ballot
from ..serializers import BallotSerializer  # noqa


class BallotViewSet(viewsets.ViewSet):
    """
    Any ballot, containing all ballot items
    ---

    retrieve:
      response_serializer: BallotSerializer
    """

    @detail_route(['GET'])
    def retrieve(self, request, ballot_id, locality_id=None):
        """
        Get metadata and list of ballot items
        """
        ballot = get_object_or_404(Ballot, id=ballot_id)
        return Response(BallotSerializer(ballot).data)
        # return Response({
        #     'ballot_id': ballot_id,
        #     'locality_id': int(locality_id or 1),
        #     'date': '2015/11/02',
        #     'ballot_items': [
        #         {
        #             'id': 1,
        #             'type': 'office',
        #             'name': 'Mayor'
        #         },
        #         {
        #             'id': 2,
        #             'type': 'office',
        #             'name': 'City Auditor'
        #         },
        #         {
        #             'id': 3,
        #             'type': 'office',
        #             'name': 'City Treasurer'
        #         },
        #         {
        #             'id': 4,
        #             'type': 'office',
        #             'name': 'Distrit 1 City Council'
        #         },
        #         {
        #             'id': 5,
        #             'type': 'office',
        #             'name': 'Distrit 3 City Council'
        #         },
        #         {
        #             'id': 6,
        #             'type': 'office',
        #             'name': 'Distrit 5 City Council'
        #         },
        #         {
        #             'id': 7,
        #             'type': 'referendum',
        #             'name': 'Measure AA'
        #         },
        #         {
        #             'id': 8,
        #             'type': 'referendum',
        #             'name': 'Measure BB'
        #         },
        #         {
        #             'id': 9,
        #             'type': 'referendum',
        #             'name': 'Measure CC'
        #         }
        #     ]
        # })



class CurrentBallotViewSet(BallotViewSet):
    """
    Current ballot, containing all ballot items
    ---

    current_ballot:
      response_serializer: BallotSerializer
    """

    @detail_route(['GET'])
    def current_ballot(self, request, locality_id):
        """
        Get the currently active ballot
        """
        return super(CurrentBallotViewSet, self).retrieve(
            request=request, ballot_id=1, locality_id=locality_id)
