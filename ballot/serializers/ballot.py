from rest_framework import serializers


class ReferendumSerializer(serializers.Serializer):
    measure_id = serializers.CharField(max_length=50)
    locality_id = serializers.CharField(max_length=50)
    number = serializers.CharField(max_length=10)
    full_text = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=10)
    supporting_count = serializers.IntegerField()
    opposing_count = serializers.IntegerField()


class BallotSerializer(serializers.Serializer):
    ballot_id = serializers.CharField(max_length=50)
    locality_id = serializers.CharField(max_length=50)
    contests = serializers.ListField(
        child=serializers.DictField())
