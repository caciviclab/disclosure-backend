from rest_framework import serializers


class LocalitySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1024)
    type = serializers.CharField(max_length=128)
    id = serializers.IntegerField()
