from rest_framework import serializers

from finance.models import Beneficiary


class BeneficiaryMoneyReceivedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField(max_length=100, source='get_type_display')
    name = serializers.CharField(max_length=100)
    contributions_received = serializers.FloatField(source='get_total_contributions_received')

    class Meta:
        model = Beneficiary
