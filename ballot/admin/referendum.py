from django.contrib import admin

from ..models import referendum as models
from _django_utils import validate_and_register_admin


class ReferendumAdmin(admin.ModelAdmin):
    # We don't want to display unnecessary or calculated fields.
    # In particular locality choices take a while to populate.
    fields = ('title', 'number', 'ballot',
              'website_url', 'facebook_url', 'twitter_url')

validate_and_register_admin(
    models.Referendum, ReferendumAdmin, num_hidden_fields=5)
