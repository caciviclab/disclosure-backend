from django.contrib import admin
from . import models


@admin.register(models.ElectionDay)
class ElectionDayAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date',)
    ordering = ('date', )
