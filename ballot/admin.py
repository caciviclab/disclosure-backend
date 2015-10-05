from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.Election)
admin.site.register(models.Ballot)
admin.site.register(models.Contest)
admin.site.register(models.Candidate)
admin.site.register(models.Referendum)
admin.site.register(models.Locality)
admin.site.register(models.Precinct)
