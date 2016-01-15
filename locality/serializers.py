from rest_framework import serializers


class LocalitySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1024)
    id = serializers.IntegerField()
