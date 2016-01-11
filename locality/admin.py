from django.contrib import admin

from . import models

admin.site.register(models.Locality)
admin.site.register(models.City)
admin.site.register(models.County)
admin.site.register(models.State)
admin.site.register(models.ZipCode)
