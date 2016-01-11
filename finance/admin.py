from django.contrib import admin

from . import models

admin.site.register(models.Form)
admin.site.register(models.PersonBenefactor)
admin.site.register(models.CorporationBenefactor)
admin.site.register(models.CommitteeBenefactor)
admin.site.register(models.Beneficiary)
admin.site.register(models.ReportingPeriod)
admin.site.register(models.IndependentMoney)
