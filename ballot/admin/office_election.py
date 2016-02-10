from django.contrib import admin

from ..models import office_election as models

admin.site.register(models.Candidate)
admin.site.register(models.OfficeElection)
