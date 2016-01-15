from django.db.models import Q
from django.http import HttpResponse, Http404

from calaccess_raw.models.campaign import RcptCd
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .serializers import ContributionSerializer
from locality.models import City
from locality.serializers import LocalitySerializer


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
def search_view(request):
    """
    Search for a location with ballot/disclosure data.
    ---
    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query
    """
    query = request.query_params.get('q', '')
    query_set = City.objects.filter(~Q(ballot=None), name__icontains=query)
    serializer = LocalitySerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def location_view(request, locality_id):
    """
    Display summarized disclosure information about a location
    ---
    parameters:
      - name: locality_id
        description: The locality_id (arbitrary, can be obtained via 'search')
        paramType: path
        type: integer
        required: true
    """
    from locality.models import City
    from ballot.models import Ballot
    from finance.models import (IndependentMoney)
    from django.db.models import Sum, F

    # TODO: set up ElectionDay app.
    try:
        locality = City.objects.get(id=locality_id)
    except City.DoesNotExist:
        raise Http404()
    ballots = Ballot.objects.filter(locality=locality)
    if not ballots:
        ballot = None
        total_benefits = 0
        benefits_by_type = dict()
        num_contributions = 0
    else:
        ballot = ballots[0]
        benefits = IndependentMoney.objects.filter(
            beneficiary__ballot_item_selection__ballot_item__ballot=ballot)
        num_contributions = benefits.count()
        total_benefits = benefits.aggregate(total=Sum(F('amount')))['total']
        benefits_groupedby_type = benefits.values(
            'benefactor__benefactor_type').annotate(
            total=Sum(F('amount')))
        key_dict = dict(IN='individual', CO='corporation',
                        PF='recipient_committee')
        benefits_by_type = dict([(key_dict[group_data['benefactor__benefactor_type']],
                                  group_data['total'])
                                 for group_data in benefits_groupedby_type])
    return Response({
        "location": {
            "name": locality.name or locality.short_name,
            "fip_id": locality.id,
            "next_election": ballot.date if ballot else None
        },
        "contribution_total": total_benefits,
        "contribution_count": num_contributions,
        "contribution_by_type": benefits_by_type,
        "contribution_by_area": {
            "inside_location": 0.56,
            "inside_state": 0.38,
            "outside_state": 0.06
        }
    }, content_type='application/json')


def homepage_view(request):
    return HttpResponse("""
        <a href='/docs/'>Check out the API Documentation</a>
        <br/>
        <a href='/admin/'>View the admin interface / database data.</a>
    """)
