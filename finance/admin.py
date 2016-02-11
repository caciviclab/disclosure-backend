from django.contrib import admin

from . import models


class BenefactorAdmin(admin.ModelAdmin):
    exclude = ('benefactor_type',)


class CommitteeBenefactorAdmin(BenefactorAdmin):
    exclude = BenefactorAdmin.exclude + ('benefactor_locality',)

admin.site.register(models.Beneficiary)
admin.site.register(models.PersonBenefactor, BenefactorAdmin)
admin.site.register(models.PartyBenefactor, BenefactorAdmin)
admin.site.register(models.OtherBenefactor, BenefactorAdmin)
admin.site.register(models.CommitteeBenefactor, CommitteeBenefactorAdmin)
admin.site.register(models.IndependentMoney)
