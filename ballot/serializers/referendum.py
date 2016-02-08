from rest_framework import serializers

from .. import models


class ReferendumSerializer(serializers.Serializer):
    class Meta:
        model = models.Referendum
