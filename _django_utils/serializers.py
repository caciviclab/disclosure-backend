from rest_framework import serializers


def as_money(num, precision=0.01):
    if num is None:
        return None
    return round(num / precision) * precision


class MagicModelSerializer(serializers.ModelSerializer):
    """ModelSerializer with '__init__(exclude)', '__init__(rename)', Meta.rename."""

    def __init__(self, model=None, exclude=None, rename=None, *args, **kwargs):
        self.exclude = exclude or tuple()
        self.rename = rename or dict()
        return super(MagicModelSerializer, self).__init__(model, *args, **kwargs)

    def get_fields(self):
        fields = super(MagicModelSerializer, self).get_fields()

        try:
            # Removing fields: local (class-level taken care of by super call)
            for exclude_field_name in self.exclude:
                fields.pop(exclude_field_name)

            # Renaming fields: local
            for field_name, new_field_name in self.rename.items():
                fields[new_field_name] = fields.pop(field_name)

            # Renaming fields: meta
            for field_name, new_field_name in getattr(self.Meta, 'rename', dict()).items():
                fields[new_field_name] = fields.pop(field_name)

        except KeyError as ke:
            raise KeyError("%s not found; select from %s" % (ke.message, list(fields.keys())))
        return fields
