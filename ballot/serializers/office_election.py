from rest_framework import serializers

from .. import models


class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)


class CandidateSerializer(PersonSerializer):
    id = serializers.IntegerField()
    party = serializers.CharField(max_length=50, source='party.name')

    class Meta:
        model = models.Candidate


class OfficeElectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, source='office.name')
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = models.OfficeElection
