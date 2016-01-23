from django.contrib import admin

from ..models import ballot as models

admin.site.register(models.Ballot)
admin.site.register(models.BallotItem)
admin.site.register(models.BallotItemSelection)
