from rest_framework import serializers

from .models import Benefactor, Beneficiary, Committee, IndependentMoney
from _django_utils.serializers import MagicModelSerializer
from locality.serializers import LocalitySerializer


class AddressSerializer(MagicModelSerializer):
    city = serializers.CharField(max_length=50, source='city.short_name')
    state = serializers.CharField(max_length=50, source='state.short_name')
    zip_code = serializers.CharField(max_length=50, source='zip_code.short_name')


class CommitteeSerializer(AddressSerializer):
    type = serializers.CharField(source='get_type_display')
    locality = LocalitySerializer()

    class Meta:
        model = Committee


class BenefactorSerializer(MagicModelSerializer):
    benefactor_locality = serializers.CharField(max_length=50, source='benefactor_locality.name')
    benefactor_type = serializers.CharField(max_length=50, source='get_benefactor_type_display')
    name = serializers.CharField(source='__str__')
    contributions = serializers.FloatField()
    total_contributions = serializers.FloatField(source='get_contributions')

    def __init__(self, models=None, beneficiary=None, *args, **kwargs):
        self.beneficiary = beneficiary
        super(BenefactorSerializer, self).__init__(models, *args, **kwargs)

    def to_representation(self, instance):
        """
        Add the 'contributions' property to a benefactor, for this particular beneficiary.

        TODO: fix this; this is hacky.
        """
        if not hasattr(instance, 'contributions'):
            instance.contributions = instance.get_contributions(beneficiary=self.beneficiary)
        return super(BenefactorSerializer, self).to_representation(instance)

    class Meta:
        model = Benefactor


class BeneficiarySerializer(MagicModelSerializer):
    class Meta:
        model = Beneficiary


class IndependentMoneySerializer(MagicModelSerializer):
    benefactor = BenefactorSerializer()
    beneficiary = BeneficiarySerializer()

    class Meta:
        model = IndependentMoney
        exclude = ('benefactor_zip',)
