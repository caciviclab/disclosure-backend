from django.contrib import admin

from ..models import office_election as models


class CandidateAdmin(admin.ModelAdmin):
    # We don't want to display unnecessary or calculated fields.
    # In particular locality choices take a while to populate.
    fields = ('ballot_item', 'first_name', 'middle_name', 'last_name', 'party',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')

    assert len(models.Candidate._meta.get_fields()) - len(fields) == 4, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.Candidate._meta.get_fields()))


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.OfficeElection)
