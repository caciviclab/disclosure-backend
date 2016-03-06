from rest_framework import serializers

from .. import models
from _django_utils.serializers import ExtendedModelSerializer


class CandidateSerializer(ExtendedModelSerializer):
    party = serializers.CharField(max_length=50, source='party.name')

    class Meta:
        model = models.Candidate


class OfficeElectionSerializer(ExtendedModelSerializer):
    name = serializers.CharField(max_length=50, source='office.name')

    class Meta:
        model = models.OfficeElection
        exclude = ('contest_type',)
        rename = dict(ballot='ballot_id')
