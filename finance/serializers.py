from rest_framework import serializers

from .models import IndependentMoney, Committee


class IndependentMoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = IndependentMoney


class CommitteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Committee
