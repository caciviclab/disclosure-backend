from django.contrib import admin

from ..models import office_election as models

admin.site.register(models.Party)
admin.site.register(models.Office)
admin.site.register(models.Candidate)
