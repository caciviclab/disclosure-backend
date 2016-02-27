from django.contrib import admin

from . import models


class ElectionDayAdmin(admin.ModelAdmin):
    list_display = ('Ballot.date', 'Ballot.locality')
admin.site.register(models.ElectionDay, ElectionDayAdmin)
