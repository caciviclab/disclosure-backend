from rest_framework import serializers


class MagicModelSerializerializer(serializers.ModelSerializer):
    """ModelSerializer with 'Meta.exclude_fields', 'Meta.renamed_fields' properties."""

    def __init__(self, model=None, exclude_fields=None, rename_fields=None, *args, **kwargs):
        self.exclude_fields = exclude_fields or getattr(self.Meta, 'exclude_fields', [])
        self.rename_fields = rename_fields or getattr(self.Meta, 'rename_fields', dict())
        return super(MagicModelSerializerializer, self).__init__(model, *args, **kwargs)

    def get_fields(self):
        fields = super(MagicModelSerializerializer, self).get_fields()

        # Removing fields
        for exclude_field_name in self.exclude_fields:
            fields.pop(exclude_field_name)

        # Renaming fields
        for field_name, new_field_name in self.rename_fields.items():
            fields[new_field_name] = fields.pop(field_name)

        return fields
