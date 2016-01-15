"""
Models related to campaign finance for referendum choices and candidates.
"""

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from locality.models import AddressMixin
from office_election.models import SocialMediaMixin, PersonMixin


@python_2_unicode_compatible
class Committee(SocialMediaMixin, AddressMixin):
    """
    Official entity that spends money in support or
    opposition to a ballot item response. Primarily-formed
    committees have official designations.
    """
    COMMITTEE_TYPES = (
        ('OF', 'Primarily-formed Official Committee'),
        ('PF', 'Primarily-formed Committee'),
        ('IC', 'Independent Committee')
    )
    name = models.CharField(max_length=255)
    filer_id = models.CharField(max_length=16, null=True, default=None,
                                help_text="Official government ID "
                                          "(none if unknown)")
    type = models.CharField(max_length=2, choices=COMMITTEE_TYPES)
    locality = models.ForeignKey('locality.Locality', null=True, default=None)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CorporationMixin(SocialMediaMixin, AddressMixin):
    """
    Information about a corporation.
    """
    name = models.CharField(max_length=255)
    locality = models.ForeignKey('locality.Locality', null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form(models.Model):
    """
    Information about finance reporting forms.
    """
    FREQUENCY_TYPES = (
        ('24', '24 hours'),
        ('SA', 'Semi-annual'),
        ('QU', 'Quarterly'),
        ('OT', 'Other')
    )

    name = models.CharField(max_length=255)
    text_id = models.CharField(max_length=32, help_text='e.g. 460 Schedule A')
    submission_frequency = models.CharField(
        max_length=2, choices=FREQUENCY_TYPES)
    locality = models.ForeignKey('locality.Locality', null=True, default=None,
                                 help_text="Only set when a form is specific "
                                           "to a locality.")

    def __str__(self):
        return self.name


class Benefactor(models.Model):
    """
    Main list of benefactors.
    """
    BENEFACTOR_TYPES = (
        ('PF', 'Primarily-formed committee'),
        ('IF', 'Independently-formed committee'),
        ('IN', 'Individual'),
        ('CO', 'Corporation'),
        ('OT', 'Other')
    )
    benefactor_id = models.AutoField(primary_key=True)  # avoids id clash
    benefactor_type = models.CharField(max_length=2, choices=BENEFACTOR_TYPES)
    benefactor_locality = models.ForeignKey(
        'locality.Locality', null=True, default=None)


class PersonBenefactor(Benefactor, PersonMixin):
    """
    Individual who contributes to a committee.
    """
    occupation = models.CharField(max_length=64, null=True)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = 'IN'


class CorporationBenefactor(Benefactor, CorporationMixin):
    """
    Corporation that contributes to a committee.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = 'CO'
        self.benefactor_locality = self.locality


class CommitteeBenefactor(Benefactor, Committee):
    """
    Committee that contributes to another committee, or
    spends on behalf of another committee.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.benefactor_type = self.type
        self.benefactor_locality = self.locality


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

    class Meta:
        verbose_name_plural = 'beneficiaries'


class ReportingPeriod(models.Model):
    """Model tracking form reporting periods."""
    period_start = models.DateField()
    period_end = models.DateField()
    form = models.ForeignKey('Form')


@python_2_unicode_compatible
class IndependentMoney(models.Model):
    """
    """
    SOURCE_TYPES = (
        ('NF', 'Netfile'),
    )
    amount = models.FloatField(help_text="Monetary value of the benefit.")
    reporting_period = models.ForeignKey('ReportingPeriod')
    report_date = models.DateField()

    benefactor_zip = models.ForeignKey('locality.ZipCode')
    benefactor = models.ForeignKey('Benefactor', help_text='Gave the benefit')
    beneficiary = models.ForeignKey('Beneficiary', help_text='Got the benefit')

    source = models.CharField(
        max_length=2, choices=SOURCE_TYPES, help_text="e.g. Netfile")
    source_xact_id = models.CharField(
        max_length=32, help_text="Transaction ID (specific to data source)")

    def __str__(self):
        val = "%s gave %s to %s @ %s" % (self.benefactor, self.amount,
                                         self.beneficiary, self.benefactor_zip)
        if self.beneficiary.ballot_item_selection is not None:
            val += " in %s %s" % (
                'support of' if self.beneficiary.support else 'opposition to',
                self.beneficiary.ballot_item_selection)
        val += ", reported via %s on %s" % (
            self.reporting_period.form, self.report_date)
        return val

    class Meta:
        verbose_name_plural = 'independent money'
