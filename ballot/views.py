from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import models
from serializers import ElectionSerializer


class Election(viewsets.ViewSet):
    """
    TODO: Figure out what should be returned here.
    ---
    list:
      response_serializer: ElectionSerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = models.Election.objects.all()

    def list(self, request, format=None):
        obj = models.Election.objects.all()
        return Response(ElectionSerializer(obj, many=True).data)
