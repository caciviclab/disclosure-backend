from django.db.models import F, Sum
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import Benefactor, Beneficiary, Committee, IndependentMoney
from .serializers import BenefactorSerializer, CommitteeSerializer, IndependentMoneySerializer
from _django_utils.serializers import as_money
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
    contributions:
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


def summarize_money(locality, benefits):
    # Simple measures
    num_contributions = benefits.count()
    total_benefits = benefits.aggregate(total=Sum(F('amount')))['total']

    # Summary measures by benefactor type
    key_map = dict(IN='individual', CO='corporation',
                   PF='recipient_committee', PY='political_party',
                   IC='independent_committee')
    benefits_groupedby_type = benefits \
        .values_list('benefactor__benefactor_type') \
        .annotate(total=Sum(F('amount')))
    benefits_by_type = dict([(key_map[vals[0]], as_money(vals[1]))  # alias keys
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
        [(key, as_money(val.aggregate(tot=Sum(F('amount')))['tot'] or 0))  # 0 for empty
         for key, val in results_by_locality.items()])

    return {  # done, manually
        "location": {
            "name": locality.name or locality.short_name,
            "id": locality.id,
        },
        "contribution_total": as_money(total_benefits),
        "contribution_count": as_money(num_contributions),
        "contribution_by_type": benefits_by_type,
        "contribution_by_area": total_by_locality,
    }


class BeneficiaryViewSet(viewsets.ViewSet):
    """
    Benefits received: contributions or independent expenditures
    ---

    contributors:
        response_serializer: BenefactorSerializer

    contributions_received:
        response_serializer: IndependentMoneySerializer
    """
    renderer_classes = [JSONRenderer]

    @list_route(['GET'])
    def contributors(self, request, committee_id):
        """List of all contributors to a committee."""
        beneficiary = get_object_or_404(Beneficiary, id=committee_id)
        benefits = Benefactor.objects.filter(independentmoney__beneficiary=beneficiary)
        return Response(BenefactorSerializer(benefits, many=True).data)

    @list_route(['GET'])
    def contributions_received(self, request, committee_id):
        """List of all benefits received by a committee."""
        beneficiary = get_object_or_404(Beneficiary, id=committee_id)
        benefits = IndependentMoney.objects.filter(beneficiary=beneficiary)
        return Response(IndependentMoneySerializer(benefits, many=True).data)

    @detail_route(['GET'])
    def summary(self, request, committee_id):
        """Aggregate benefits, over all contributions to a committee."""
        beneficiary = get_object_or_404(Beneficiary, id=committee_id)
        benefits = IndependentMoney.objects.filter(beneficiary=beneficiary)
        locality = beneficiary.locality.reverse_lookup()  # upgrade

        summary_dict = summarize_money(locality=locality, benefits=benefits)
        return Response(summary_dict)
