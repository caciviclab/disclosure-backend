from .. import models
from _django_utils.serializers import ExtendedModelSerializer


class ReferendumSerializer(ExtendedModelSerializer):
    class Meta:
        model = models.Referendum
        exclude = ('contest_type',)
        rename = dict(ballot='ballot_id')
