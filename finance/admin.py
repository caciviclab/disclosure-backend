from django.contrib import admin

from . import models


class CommitteeBenefactorAdmin(admin.ModelAdmin):
    # We don't want to display unnecessary or calculated fields.
    # In particular locality choices take a while to populate.
    # Also put the fields in a logical order for filling the form.
    fields = ('name', 'type', 'filer_id', 'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')

    assert len(models.CommitteeBenefactor._meta.get_fields()) - \
        len(fields) == 9, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.CommitteeBenefactor._meta.get_fields()))


class OtherBenefactorAdmin(admin.ModelAdmin):
    fields = ('name', 'benefactor_type', 'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')

    assert len(models.OtherBenefactor._meta.get_fields()) - \
        len(fields) == 6, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.OtherBenefactor._meta.get_fields()))


class PersonBenefactorAdmin(admin.ModelAdmin):
    fields = ('first_name', 'middle_name', 'last_name', 'occupation',
              'benefactor_type', 'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')

    assert len(models.PersonBenefactor._meta.get_fields()) - \
        len(fields) == 5, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.PersonBenefactor._meta.get_fields()))


class BeneficiaryAdmin(admin.ModelAdmin):
    fields = ('name', 'type', 'filer_id', 'support', 'ballot_item_selection',
              'street', 'city', 'zip_code',
              'photo_url', 'website_url', 'facebook_url', 'twitter_url')

    assert len(models.Beneficiary._meta.get_fields()) - \
        len(fields) == 5, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.Beneficiary._meta.get_fields()))


class IndependentMoneyAdmin(admin.ModelAdmin):
    fields = ('benefactor', 'benefactor_zip', 'beneficiary',
              'amount', 'cumulative_amount', 'report_date', 'reporting_period',
              'source', 'source_xact_id')

    assert len(models.IndependentMoney._meta.get_fields()) - \
        len(fields) == 1, \
        "Make sure there are no new fields. %r %r " % \
        (len(fields), len(models.IndependentMoney._meta.get_fields()))


admin.site.register(models.Beneficiary, BeneficiaryAdmin)
admin.site.register(models.PersonBenefactor, PersonBenefactorAdmin)
admin.site.register(models.OtherBenefactor, OtherBenefactorAdmin)
admin.site.register(models.CommitteeBenefactor, CommitteeBenefactorAdmin)
admin.site.register(models.IndependentMoney, IndependentMoneyAdmin)
