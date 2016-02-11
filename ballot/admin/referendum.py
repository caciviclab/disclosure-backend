from django.contrib import admin

from ..models import referendum as models


class ReferendumAdmin(admin.ModelAdmin):
    # We don't want to display unnecessary or calculated fields.
    # In particular locality choices take a while to populate.
    fields = ('title', 'number', 'ballot',
              'website_url', 'facebook_url', 'twitter_url')

    assert len(models.Referendum._meta.get_fields()) - len(fields) == 5, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.Referendum._meta.get_fields()))


admin.site.register(models.Referendum, ReferendumAdmin)
