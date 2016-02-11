from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ..serializers import ReferendumSerializer  # noqa


class ReferendumViewSet(viewsets.ViewSet):
    """
    Referendum
    ---

    retrieve:
        response_serializer: ReferendumSerializer
    """

    @detail_route(['GET'])
    def retrieve(self, request, referendum_id, locality_id=None):
        """
        Referendum text / details
        ---
        """
        return Response({
            'id': int(referendum_id),
            'number': 'BB',
            'title': 'Ethics Commission Authority Increase Charter Amendment',
        })
