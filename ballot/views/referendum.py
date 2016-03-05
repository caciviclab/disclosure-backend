from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Referendum
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
        Details for a single referendum.
        ---
        """
        referendum = get_object_or_404(Referendum, id=referendum_id)
        return Response(ReferendumSerializer(referendum).data)
