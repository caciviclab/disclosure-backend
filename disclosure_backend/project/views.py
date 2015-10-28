from calaccess_raw.models.campaign import RcptCd
from django.http import HttpResponse
from serializers import ContributionSerializer, LocationSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class Contribution(viewsets.ViewSet):
    """
    A contribution is money that an filing committee has received.
    ---
    retrieve:
      response_serializer: ContributionSerializer
    list:
      response_serializer: ContributionSerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = RcptCd.objects.all()

    def list(self, request):
        """ List all contributions """
        obj = RcptCd.objects.all()[1:10]
        return Response(ContributionSerializer(obj, many=True).data)

    def retrieve(self, request, pk=None, format=None):
        """ Get a single contribution """
        obj = RcptCd.objects.get(id=pk)
        return Response(ContributionSerializer(obj).data)


@api_view(['GET'])
def location_view(request, fip_id=None):
    """
    Display summarized information about a location
    NOTE: This is stubbed to always return the same thing.
    ---
    parameters:
      - name: fip_id
        type: string
    response_serializer: LocationSerializer
    """
    return Response({
        "countyName": "san francisco",
        "type": "county",
        "fip_id": "6075",
        "ofState": {
            "stateName": "california",
            "type": "state",
            "id": "6"
        },
        "collectsCampaignFinanceData": "",
        "campaignFinanceDataSources": [{"name": "", "href": ""}],
        "electionDataSummary": {
            "hasElectionData": "",
            "isOnline": "",
            "isPubliclyAccessible": "",
            "isMachineReadable": "",
            "pastElectionData": {
                "hasPastElectionData": "",
                "yearsPastElectionDataCollected": [
                    {"year": "", "isFiledOnline": "", "isPubliclyAccessible": "", "isMachineReadable": ""}
                ],
                "pastElectionDataSources": [{"name": "", "href": ""}]
            },
            "upcomingElectionData": {
                "hasUpcomingElectionData": "",
                "isCollectingUpcomingElectionData": "",
                "dataCollectionStartDate": "DD/MM/YYYY",
                "dataCollectionEndDate": "DD/MM/YYYY",
                "dataFiledOnline": "",
                "dataPubliclyAccessible": "",
                "dataMachineReadable": "",
                "dataUpdateFrequency": ""
            }
        },
        "hasCities": [
            {"cityName": "", "type": "city", "id": "6_**_**"}
        ]
    }, content_type='application/json')


def homepage_view(request):
    return HttpResponse("<a href='/docs/'>Check out the API Documentation</a>")


@api_view(['GET'])
def search_view(request):
    """
    Search for a location (or later, a person or ballot measure).
    NOTE: This endpoint is currently stubbed.
    ---
    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query
    """
    return Response([{"name": "San Francisco", "fip_id": "6075"}])
