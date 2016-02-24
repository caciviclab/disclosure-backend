from django.contrib import admin

from ..models import ballot as models


admin.site.register(models.Ballot)
