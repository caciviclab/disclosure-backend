from rest_framework import serializers
from ..models import Ballot, BallotItem
from _django_utils import MagicModelSerializerializer


class BallotItemSerializer(MagicModelSerializerializer):
    contest_type = serializers.CharField(source='get_contest_type_display')

    class Meta:
        model = BallotItem


class BallotSerializer(MagicModelSerializerializer):
    ballot_items = BallotItemSerializer(many=True, read_only=True, exclude_fields=['ballot'])

    class Meta:
        model = Ballot
        rename_fields = dict(locality='locality_id')
