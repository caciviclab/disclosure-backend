from .. import models
from _django_utils.serializers import MagicModelSerializer


class ReferendumSerializer(MagicModelSerializer):
    class Meta:
        model = models.Referendum
        exclude_fields = ('contest_type',)
        rename_fields = dict(ballot='ballot_id')
