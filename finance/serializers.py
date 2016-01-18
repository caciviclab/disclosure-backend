from rest_framework import serializers

from .models import IndependentMoney


class IndependentMoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = IndependentMoney
