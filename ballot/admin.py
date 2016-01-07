from django.contrib import admin
import models

admin.site.register(models.Ballot)
admin.site.register(models.Contest)
admin.site.register(models.Referendum)


@admin.register(models.Election)
class ElectionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date',)
    ordering = ('date', )
