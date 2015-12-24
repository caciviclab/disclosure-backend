from django.contrib import admin
import models

admin.site.register(models.Ballot)
admin.site.register(models.Contest)
admin.site.register(models.Candidate)
admin.site.register(models.Referendum)
admin.site.register(models.Locality)
admin.site.register(models.Precinct)


@admin.register(models.Election)
class ElectionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date',)
    ordering = ('date', )
