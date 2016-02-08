from rest_framework import serializers


class BenefactorSummarySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1024)
    contributions = serializers.FloatField()
