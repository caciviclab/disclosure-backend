from rest_framework import serializers

from .models import Benefactor, Beneficiary, Committee, IndependentMoney
from _django_utils.serializers import MagicModelSerializerializer
from locality.serializers import LocalitySerializer


class AddressSerializer(MagicModelSerializerializer):
    city = serializers.CharField(max_length=50, source='city.short_name')
    state = serializers.CharField(max_length=50, source='state.short_name')
    zip_code = serializers.CharField(max_length=50, source='zip_code.short_name')


class CommitteeSerializer(AddressSerializer):
    type = serializers.CharField(source='get_type_display')
    locality = LocalitySerializer()

    class Meta:
        model = Committee


class BenefactorSerializer(MagicModelSerializerializer):
    benefactor_locality = serializers.CharField(max_length=50, source='benefactor_locality.name')

    class Meta:
        model = Benefactor
        exclude_fields = ('benefactor_type',)


class BeneficiarySerializer(MagicModelSerializerializer):
    class Meta:
        model = Beneficiary


class IndependentMoneySerializer(MagicModelSerializerializer):
    benefactor = BenefactorSerializer()
    beneficiary = BeneficiarySerializer()

    class Meta:
        model = IndependentMoney
