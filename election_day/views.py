from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ballot.models import Ballot
from .serializers import ElectionDaySerializer


class ElectionDay(viewsets.ViewSet):
    """
    TODO: Figure out what should be returned here.
    ---
    list:
      response_serializer: ElectionDaySerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = Ballot.objects.all()

    def list(self, request, format=None):
        obj = Ballot.objects.all()
        return Response(ElectionDaySerializer(obj, many=True).data)
