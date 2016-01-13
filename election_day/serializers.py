from rest_framework import serializers
from .models import ElectionDay


class ElectionDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectionDay
