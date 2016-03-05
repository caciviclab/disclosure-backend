from .. import models
from _django_utils.serializers import MagicModelSerializerializer


class ReferendumSerializer(MagicModelSerializerializer):
    class Meta:
        model = models.Referendum
        exclude_fields = ('contest_type',)
        rename_fields = dict(ballot='ballot_id')
