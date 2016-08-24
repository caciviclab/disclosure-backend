from rest_framework import serializers

from .. import models


class ReferendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Referendum
        exclude = ('ballot',)
