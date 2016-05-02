import os

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from rest_framework import viewsets
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response

from .serializers import BeneficiaryMoneyReceivedSerializer
from ballot.models import Ballot, BallotItemSelection
from finance.models import Beneficiary, IndependentMoney
from finance.views import summarize_money
from locality.models import Locality
from locality.serializers import LocalitySerializer
from swagger_nickname_registry import swagger_nickname


@api_view(['GET'])
@swagger_nickname('search')
def search_view(request):
    """
    List of locations with ballot/disclosure data.
    ---

    parameters:
      - name: q
        description: The user's search query
        type: string
        paramType: query

    response_serializer:
        LocalitySerializer
    """
    query = request.query_params.get('q', '')
    query_set = Locality.objects.filter(~Q(ballot=None), name__icontains=query)
    serializer = LocalitySerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@swagger_nickname('disclosure_summary')
def locality_disclosure_summary_view(request, ballot_id):
    """
    Summarized disclosure information for a ballot
    ---
    parameters:
      - name: ballot_id
        description: The ballot_id
        paramType: path
        type: integer
        required: true
    """
    # TODO: set up ElectionDay app.
    ballot = get_object_or_404(Ballot, id=ballot_id)
    locality = Locality.objects.get(id=ballot.locality_id).reverse_lookup()

    # Get all relevant rows of IndependentMoney
    benefits = IndependentMoney.objects.filter(
        beneficiary__ballot_item_selection__ballot_item__ballot=ballot)

    data_dict = summarize_money(locality=locality, benefits=benefits)
    data_dict['location']['next_election_date'] = ballot.date if ballot else None

    return Response(data_dict)
    """
    return Response({  # done, manually
        "location": {
            "name": locality.name or locality.short_name,
            "id": locality.id,
            "next_election_date": ballot.date if ballot else None
        },
        "contribution_total": total_benefits,
        "contribution_count": num_contributions,
        "contribution_by_type": benefits_by_type,
        "contribution_by_area": total_by_locality,
    })
    """


class BallotItemSelectionViewSet(viewsets.ViewSet):
    """
    Abstract class serving both candidates and referendums
    """
    def _show_relevant_beneficiaries(self, request, ballot_item_selection_id, supporting):
        ballot_item_selection = get_object_or_404(BallotItemSelection, id=ballot_item_selection_id)
        beneficiary = Beneficiary.objects.filter(
            ballot_item_selection=ballot_item_selection,
            support=supporting)
        return Response(BeneficiaryMoneyReceivedSerializer(beneficiary, many=True).data)

    @list_route(['GET'])
    def supporting(self, request, ballot_item_selection_id):
        """
        List of supporting committees, and level of benefits given.

        response_serializer: CommitteeWithContributionsSerializer
        """
        return self._show_relevant_beneficiaries(
            request=request,
            ballot_item_selection_id=ballot_item_selection_id,
            supporting=True)

    @list_route(['GET'])
    def opposing(self, request, ballot_item_selection_id):
        """
        List of opposing committees, and level of benefits given.
        """
        return self._show_relevant_beneficiaries(
            request=request,
            ballot_item_selection_id=ballot_item_selection_id,
            supporting=False)


class ReferendumViewSet(BallotItemSelectionViewSet):
    """
    Money surrounding particular referendums.
    ---

    supporting:
        response_serializer: BeneficiaryMoneyReceivedSerializer

    opposing:
        response_serializer: BeneficiaryMoneyReceivedSerializer
    """
    @list_route(['GET'])
    def supporting(self, request, referendum_id):
        """
        List of committees supporting a referendum, and level of benefits given.
        """
        # ballot_item_selection_id =   # query from referendumresponse model
        return super(ReferendumViewSet, self).supporting(
            request, ballot_item_selection_id=referendum_id)

    @list_route(['GET'])
    def opposing(self, request, referendum_id):
        """
        List of committees opposing a referendum, and level of benefits given.
        """
        # ballot_item_selection_id =   # query from referendumresponse model
        return super(ReferendumViewSet, self).opposing(
            request, ballot_item_selection_id=referendum_id)


class CandidateViewSet(BallotItemSelectionViewSet):
    """
    Money surrounding particular candidates.
    ---

    supporting:
        response_serializer: BeneficiaryMoneyReceivedSerializer

    opposing:
        response_serializer: BeneficiaryMoneyReceivedSerializer
    """
    @list_route(['GET'])
    def supporting(self, request, candidate_id):
        """
        List of committees supporting a candidate, and level of benefits given.
        """
        return super(CandidateViewSet, self).supporting(
            request, ballot_item_selection_id=candidate_id)

    @list_route(['GET'])
    def opposing(self, request, candidate_id):
        """
        List of committees opposing a candidate, and level of benefits given.
        """
        return super(CandidateViewSet, self).opposing(
            request, ballot_item_selection_id=candidate_id)


def homepage_view(request):
    template = loader.get_template('homepage.html')
    template_context = {}
    if settings.CRON_LOGS_DIR:
        template_context['cronjobs'] = []
        cronlogs = os.listdir(settings.CRON_LOGS_DIR)
        for cronlog in cronlogs:
            cronlog_filepath = os.path.join(settings.CRON_LOGS_DIR, cronlog)

            # On the deploy host, we archive old logs into an "archive" folder.
            # Skip that folder.
            if os.path.isdir(cronlog_filepath):
                continue

            with open(cronlog_filepath, 'r') as f:
                template_context['cronjobs'] += [f.read()]
    return HttpResponse(template.render(template_context, request))
