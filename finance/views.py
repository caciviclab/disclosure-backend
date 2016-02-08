from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import Committee, IndependentMoney
from .serializers import CommitteeSerializer, IndependentMoneySerializer
from swagger_nickname_registry import swagger_nickname


class CommitteeViewSet(viewsets.ViewSet):
    """
    Committee collects donations
    ---
    retrieve:
        response_serializer: CommitteeSerializer
    """
    queryset = Committee.objects.all()

    def retrieve(self, request, committee_id):
        """A single committee"""
        obj = get_object_or_404(Committee, id=committee_id)
        return Response(CommitteeSerializer(obj).data)


class BenefactorViewSet(viewsets.ViewSet):
    """
    Benefits given: contributions and independent expenditures
    ---
    list:
      response_serializer: IndependentMoneySerializer
    """
    renderer_classes = [JSONRenderer]
    queryset = IndependentMoney.objects.all()

    @list_route(['GET'])
    @swagger_nickname('contributions')
    def list(self, request, committee_id):
        """List all contributions made"""
        obj = IndependentMoney.objects.filter(
            benefactor__committeebenefactor__id=committee_id)
        return Response(IndependentMoneySerializer(obj, many=True).data)


class BeneficiaryViewSet(viewsets.ViewSet):
    """
    Benefits received: contributions or independent expenditures
    """
    renderer_classes = [JSONRenderer]

    @list_route(['GET'])
    def list(self, request, committee_id):
        """List all benefits received."""
        return Response([
            {
                'name': 'Some Other Committee',
                'type': 'committee',
                'expenditures': 700,
            },
            {
                'name': 'Samantha Brooks',
                'type': 'individual',
                'contributions': 700,
            },
            {
                'name': 'Some Committee',
                'type': 'committee',
                'contributions': 700,
            },
            {
                'name': 'Democratic Party of California',
                'type': 'political_party',
                'contributions': 700,
            }
        ])

    @detail_route(['GET'])
    def summary(self, request, committee_id):
        """Summarize over all contributions"""
        return Response({
            'contribution_by_type': {
                'benefactor_type'
                'unitemized': 2916394,
                'self_funded': 512554,
                'political_party': 6426112,
                'individual': 11134547,
                'recipient_committee': 986229,
            },
            'contribution_by_area': {
                'inside_location': 0.56,
                'inside_state': 0.38,
                'outside_state': 0.06
            }
        })
