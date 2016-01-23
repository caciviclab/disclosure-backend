from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def measure_view(request, measure_id):
    """
    Display summarized disclosure information about a committee
    ---
    parameters:
      - name: measure_id
        description: The measure_id
        paramType: path
        type: integer
        required: true
    """
    return Response({
        'measure_id': 1,
        'city': {
            'fips_id': 6075,
            'location': {
                'name': 'San Francisco'
            }
        },  # Not sure if city really makes sense here
        'number': 'BB',
        'full_text': 'Shall the Charter of the City of Oakland be amended to '
                     ' provide the Public Ethics Commission greater '
                     'independence, broader enforcement authority, powers',
        'title': 'Ethics Commission Authority Increase Charter Amendment',
        'supporting_count': 4,
        'opposing_count': 6
    }, content_type='application/json')


@api_view(['GET'])
def ballot_view(request, locality_id):
    """
    Display summarized ballot information
    """
    return Response({
        'ballot_id': 'ballot1',
        'locality_id': 'locality2',
        'contests': [
            {
                'contest_type': 'office',
                'name': 'Mayor'
            },
            {
                'contest_type': 'office',
                'name': 'City Auditor'
            },
            {
                'contest_type': 'office',
                'name': 'City Treasurer'
            },
            {
                'contest_type': 'office',
                'name': 'Distrit 1 City Council'
            },
            {
                'contest_type': 'office',
                'name': 'Distrit 3 City Council'
            },
            {
                'contest_type': 'office',
                'name': 'Distrit 5 City Council'
            },
            {
                'contest_type': 'referendum',
                'name': 'Measure AA'
            },
            {
                'contest_type': 'referendum',
                'name': 'Measure BB'
            },
            {
                'contest_type': 'referendum',
                'name': 'Measure CC'
            }
        ]
    }, content_type='application/json')
