from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import IndependentMoney
from .serializers import IndependentMoneySerializer


class IndependentMoneyViewSet(viewsets.ViewSet):
    """
    A contribution is money that a filing committee has received.
    ---
    retrieve:
      response_serializer: IndependentMoneySerializer
    list:
      response_serializer: IndependentMoneySerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = IndependentMoney.objects.all()

    def list(self, request):
        """ List all contributions """
        obj = IndependentMoney.objects.all()[1:10]
        return Response(IndependentMoneySerializer(obj, many=True).data)

    def retrieve(self, request, pk=None, format=None):
        """ Get a single contribution """
        obj = IndependentMoney.objects.get(id=pk)
        return Response(IndependentMoneySerializer(obj).data)
