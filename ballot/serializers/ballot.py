from rest_framework import serializers
from ..models import Ballot, BallotItem
from _django_utils import ExtendedModelSerializer


class BallotItemSerializer(ExtendedModelSerializer):
    contest_type = serializers.CharField(source='get_contest_type_display')
    name = serializers.CharField(source='__str__')

    class Meta:
        model = BallotItem


class BallotSerializer(ExtendedModelSerializer):
    ballot_items = BallotItemSerializer(many=True, read_only=True, exclude=['ballot'])

    class Meta:
        model = Ballot
        rename = dict(locality='locality_id')
