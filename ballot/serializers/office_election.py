from rest_framework import serializers

from .. import models


class CandidateSerializer(serializers.ModelSerializer):
    party = serializers.CharField(max_length=50, source='party.name')

    class Meta:
        model = models.Candidate


class OfficeElectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, source='office.name')

    class Meta:
        model = models.OfficeElection
        exclude_fields = ['contest_type']
        rename_fields = dict(ballot='ballot_id')
