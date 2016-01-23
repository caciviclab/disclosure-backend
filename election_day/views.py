from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import ElectionDay
from .serializers import ElectionDaySerializer


class ElectionDayView(viewsets.ViewSet):
    """
    TODO: Figure out what should be returned here.
    ---
    list:
      response_serializer: ElectionDaySerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = ElectionDay.objects.all()

    def list(self, request, format=None):
        obj = ElectionDay.objects.all()
        return Response(ElectionDaySerializer(obj, many=True).data)
