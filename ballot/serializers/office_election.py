from rest_framework import serializers

from .. import models


class OfficeElectionSerializer(serializers.Serializer):
    class Meta:
        model = models.OfficeElection


class CandidateSerializer(serializers.Serializer):
    class Meta:
        model = models.Candidate
