from django.contrib import admin

from ..models import referendum as models

admin.site.register(models.Referendum)
