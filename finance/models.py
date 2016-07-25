"""
Models related to campaign finance for referendum choices and candidates.
"""

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from _django_utils.serializers import as_money
from ballot.models import PersonMixin, SocialMediaMixin
from locality.models import AddressMixin, ReverseLookupStringMixin


@python_2_unicode_compatible
class Employer(SocialMediaMixin, AddressMixin):
    """
    Placeholder from the tran_Emp field from Netfile.
    Making a model out of it will allow explicit entity resolution.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


@python_2_unicode_compatible
class Committee(SocialMediaMixin, AddressMixin):
    """
    Official entity that spends money in support or
    opposition to a ballot item response. Primarily-formed
    committees have official designations.
    """
    COMMITTEE_TYPES = (
        ('CC', 'Candidate Controlled Committee'),
        ('PF', 'Primarily Formed Committees'),
        ('IC', 'General Purpose Committees'),
        ('BM', 'Ballot Measure Committee')
    )
    name = models.CharField(max_length=255)
    filer_id = models.CharField(max_length=16, null=True, default=None,
                                help_text="Official government ID "
                                          "(none if unknown)")
    type = models.CharField(max_length=2, choices=COMMITTEE_TYPES)
    locality = models.ForeignKey('locality.Locality', blank=True, null=True, default=None)

    def __str__(self):
        return '[%s] %s' % (self.type, self.name)

    class Meta:
        ordering = ('name', 'locality__name', 'locality__short_name')


@python_2_unicode_compatible
class OtherMixin(SocialMediaMixin, AddressMixin):
    """
    Information about a commerical entity (OTH)
    """
    name = models.CharField(max_length=255)
    locality = models.ForeignKey('locality.Locality', blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name', 'locality__name', 'locality__short_name')


@python_2_unicode_compatible
class Benefactor(models.Model, ReverseLookupStringMixin):
    """
    Main list of benefactors.
    """
    BENEFACTOR_TYPES = (
        ('PF', 'Primarily-formed committee'),
        ('IF', 'Independently-formed committee'),
        ('IN', 'Individual'),
        ('PY', 'Political Party'),
        ('OT', 'Other')
    )
    benefactor_id = models.AutoField(primary_key=True)  # avoids id clash
    benefactor_type = models.CharField(max_length=2, choices=BENEFACTOR_TYPES)
    benefactor_locality = models.ForeignKey(
        'locality.Locality', blank=True, null=True, default=None)

    def __str__(self):
        return ReverseLookupStringMixin.__str__(self)

    def get_contributions(self, beneficiary=None):
        money = IndependentMoney.objects.filter(benefactor=self)
        if beneficiary is not None:
            money = money.filter(beneficiary=beneficiary)
        total = money.aggregate(models.Sum('amount')) or 0
        return as_money(total.values()[0])

    class Meta:
        ordering = ('benefactor_locality__name',
                    'benefactor_locality__short_name')


@python_2_unicode_compatible
class PersonBenefactor(Benefactor, PersonMixin, AddressMixin):
    """
    Individual who contributes to a committee.
    """
    occupation = models.CharField(max_length=64, null=True, default=None, blank=True)
    employer = models.ForeignKey('Employer', null=True, default=None, blank=True)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = 'IN'

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return '%s @ %s' % (PersonMixin.__unicode__(self), self.benefactor_locality)

    class Meta:
        ordering = PersonMixin._meta.ordering + Benefactor._meta.ordering


@python_2_unicode_compatible
class OtherBenefactor(Benefactor, OtherMixin):
    """
    Other entity that contributes to a committee.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = 'OT'
        self.benefactor_locality = self.locality

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return OtherMixin.__unicode__(self)

    class Meta:
        ordering = Benefactor._meta.ordering + OtherMixin._meta.ordering


@python_2_unicode_compatible
class CommitteeBenefactor(Benefactor, Committee):
    """
    Committee that contributes to another committee, or
    spends on behalf of another committee.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = self.type
        self.benefactor_locality = self.locality

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return Committee.__unicode__(self)

    class Meta:
        ordering = Benefactor._meta.ordering + Committee._meta.ordering


@python_2_unicode_compatible
class PartyBenefactor(Benefactor):
    """
    Political Party that contributes to a committee.
    """
    name = models.CharField(max_length=256)
    party = models.ForeignKey('ballot.Party')

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = 'PY'

    def __str__(self):
        return '%s party' % self.name

    class Meta:
        ordering = ('name', 'party__name') + Benefactor._meta.ordering


class Beneficiary(Committee):
    """
    Committee that receives contributions or spending
    on their behalf. The benefits must be in relation
    to a specific ballit item response.
    """
    support = models.NullBooleanField(null=True, default=None,
                                      help_text="Whether funds are to support "
                                                "(Y) or oppose (N)")
    ballot_item_selection = models.ForeignKey(
        'ballot.BallotItemSelection', null=True, default=None)

    def get_total_contributions_received(self):
        money = IndependentMoney.objects.filter(beneficiary=self)
        total = money.aggregate(models.Sum('amount')) or 0
        return as_money(total.values()[0])

    class Meta:
        verbose_name_plural = 'beneficiaries'
        ordering = Committee._meta.ordering


@python_2_unicode_compatible
class IndependentMoney(models.Model):
    """
    """
    SOURCE_TYPES = (
        ('NF', 'Netfile'),
    )
    amount = models.FloatField(help_text="Monetary value of the benefit.")
    cumulative_amount = models.FloatField(
        help_text="Total monetary value of provided benefits, to date of this transaction.",
        blank=True, null=True, default=None)
    report_date = models.DateField()

    benefactor_zip = models.ForeignKey('locality.ZipCode')
    benefactor = models.ForeignKey('Benefactor', help_text='Gave the benefit')
    beneficiary = models.ForeignKey('Beneficiary', help_text='Got the benefit')

    source = models.CharField(
        max_length=2, choices=SOURCE_TYPES, help_text="e.g. Netfile")
    source_xact_id = models.CharField(
        max_length=32, help_text="Transaction ID (specific to data source)")
    unique_together = ("source", "source_xact_id")

    filing_id = models.CharField(
        max_length=32, help_text="Transaction ID (specific to government processing entity)",
        blank=True, null=True, default=None)

    def __str__(self):
        val = "[%s] gave $%.2f to [%s] @ %s" % (
            self.benefactor, float(self.amount), self.beneficiary,
            self.benefactor_zip)
        if self.beneficiary.ballot_item_selection is not None:
            val += " in %s [%s]" % (
                'support of' if self.beneficiary.support else 'opposition to',
                self.beneficiary.ballot_item_selection)
        return val

    class Meta:
        verbose_name_plural = 'independent money'
        ordering = ('-beneficiary__ballot_item_selection__ballot_item__ballot__date',  # noqa
                    '-report_date', )
