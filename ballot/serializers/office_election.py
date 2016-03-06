from rest_framework import serializers

from .. import models
from _django_utils.serializers import MagicModelSerializer


class CandidateSerializer(MagicModelSerializer):
    party = serializers.CharField(max_length=50, source='party.name')

    class Meta:
        model = models.Candidate


class OfficeElectionSerializer(MagicModelSerializer):
    name = serializers.CharField(max_length=50, source='office.name')

    class Meta:
        model = models.OfficeElection
        exclude = ('contest_type',)
        rename = dict(ballot='ballot_id')
