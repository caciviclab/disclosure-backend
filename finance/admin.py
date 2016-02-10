from django.contrib import admin

from . import models


class CommitteeBenefactorAdmin(admin.ModelAdmin):
    exclude = ('benefactor_type', 'benefactor_locality')


class OtherBenefactorAdmin(admin.ModelAdmin):
    exclude = ['benefactor_locality']


admin.site.register(models.Beneficiary)
admin.site.register(models.PersonBenefactor)
admin.site.register(models.OtherBenefactor)
admin.site.register(models.CommitteeBenefactor)
admin.site.register(models.IndependentMoney)
