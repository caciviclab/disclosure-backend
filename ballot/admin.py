from django.contrib import admin

from . import models

admin.site.register(models.Ballot)
admin.site.register(models.BallotItem)
admin.site.register(models.BallotItemSelection)
