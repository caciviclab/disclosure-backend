from django.db.models import Q
from django.http import HttpResponse, Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from locality.models import City
from locality.serializers import LocalitySerializer


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
        ballots = Ballot.objects.filter(locality=locality)
        ballot = ballots[0]
    except (City.DoesNotExist, IndexError):
        # No locality found, or no ballot exists.
        raise Http404()

    # Get all relevant rows of IndependentMoney
    benefits = IndependentMoney.objects.filter(
        beneficiary__ballot_item_selection__ballot_item__ballot=ballot)

    # Simple measures
    num_contributions = benefits.count()
    total_benefits = benefits.aggregate(total=Sum(F('amount')))['total']

    # Summary measures by benefactor type
    key_map = dict(IN='individual', CO='corporation',
                   PF='recipient_committee')
    benefits_groupedby_type = benefits \
        .values_list('benefactor__benefactor_type') \
        .annotate(total=Sum(F('amount')))
    benefits_by_type = dict([(key_map[vals[0]], vals[1])  # alias keys
                             for vals in benefits_groupedby_type])

    # Summarize by locality.
    results_by_locality = dict(
        unknown_location=benefits
        .filter(benefactor__benefactor_locality=None),
        inside_location=benefits
        .filter(benefactor__benefactor_locality=locality),
        inside_state=benefits
        .filter(benefactor__benefactor_locality__city__state=locality.state),
        outside_state=benefits
        .exclude(benefactor__benefactor_locality=None)
        .exclude(benefactor__benefactor_locality__city__state=locality.state))
    total_by_locality = dict(
        [(key, val.aggregate(tot=Sum(F('amount')))['tot'] or 0)  # 0 for empty
         for key, val in results_by_locality.items()])

    return Response({
        "location": {
            "name": locality.name or locality.short_name,
            "id": locality.id,
            "next_election": ballot.date if ballot else None
        },
        "contribution_total": total_benefits,
        "contribution_count": num_contributions,
        "contribution_by_type": benefits_by_type,
        "contribution_by_area": total_by_locality,
    }, content_type='application/json')


def homepage_view(request):
    return HttpResponse("""
        <a href='/docs/'>Check out the API Documentation</a>
        <br/>
        <a href='/admin/'>View the admin interface / database data.</a>
    """)
