from calaccess_raw.models.campaign import RcptCd
from django.http import HttpResponse
from serializers import ContributionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class Contribution(viewsets.ViewSet):
    """
    A contribution is money that an filing committee has received.
    ---
    retrieve:
      response_serializer: ContributionSerializer
      parameters:
        - name: id
          required: true
          paramType: query
    list:
      response_serializer: ContributionSerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = RcptCd.objects.all()

    def list(self, request):
        """ List all contributions """
        obj = RcptCd.objects.all()[1:10]
        return Response(ContributionSerializer(obj, many=True).data)

    def retrieve(self, request, format=None):
        """ Get a single contribution """
        obj = RcptCd.objects.get(id=request.GET['id'])
        return Response(ContributionSerializer(obj).data)


def homepage_view(request):
    return HttpResponse("<a href='/docs/'>Check out the API Documentation</a>")
