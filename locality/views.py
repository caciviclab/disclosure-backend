from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from locality.models import Locality
from locality.serializers import LocalitySerializer


class LocalityViewSet(viewsets.ViewSet):
    """
    Locality
    ---

    retrieve:
      response_serializer: LocalitySerializer
    """

    queryset = Locality.objects.all()

    def retrieve(self, request, locality_id):
        """
        Details for a locality.
        """
        obj = get_object_or_404(Locality, id=locality_id)
        return Response(LocalitySerializer(obj).data)
