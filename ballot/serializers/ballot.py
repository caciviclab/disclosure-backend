from rest_framework import serializers


class BallotSerializer(serializers.Serializer):
    date = serializers.DateField
    ballot_id = serializers.IntegerField
    locality_id = serializers.CharField(max_length=50)
    ballot_items = serializers.ListField(
        child=serializers.DictField())
