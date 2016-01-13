from rest_framework import serializers

from .models import Locality


class LocalitySerializer(serializers.Serializer):
    class Meta:
        model = Locality
