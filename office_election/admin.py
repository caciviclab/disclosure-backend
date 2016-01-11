from django.contrib import admin

from . import models

admin.site.register(models.Party)
admin.site.register(models.Office)
admin.site.register(models.Candidate)
