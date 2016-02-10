from rest_framework import serializers
from ..models import Ballot, BallotItem


class BallotItemSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    contest_type = serializers.CharField(source='get_contest_type_display')
    name = serializers.CharField(source='*', read_only=True)

    class Meta:
        model = BallotItem


class BallotSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    locality_id = serializers.CharField(max_length=50)
    date = serializers.DateField()
    ballot_items = BallotItemSerializer(many=True, read_only=True)

    class Meta:
        model = Ballot
