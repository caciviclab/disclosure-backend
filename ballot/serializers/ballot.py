from rest_framework import serializers
from ..models import Ballot, BallotItem
from _django_utils import MagicModelSerializer


class BallotItemSerializer(MagicModelSerializer):
    contest_type = serializers.CharField(source='get_contest_type_display')
    name = serializers.CharField(source='__str__')

    class Meta:
        model = BallotItem


class BallotSerializer(MagicModelSerializer):
    ballot_items = BallotItemSerializer(many=True, read_only=True, exclude_fields=['ballot'])

    class Meta:
        model = Ballot
        rename_fields = dict(locality='locality_id')
