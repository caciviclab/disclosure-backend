from rest_framework import serializers

from .. import models


class ReferendumSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=5)

    class Meta:
        model = models.Referendum
