"""
Models related to campaign finance for referendum choices and candidates.
"""

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from office_election.models import SocialMediaMixin, PersonMixin


@python_2_unicode_compatible
class Committee(SocialMediaMixin):
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
    address = models.ForeignKey('locality.Address', null=True, default=None)
    locality = models.ForeignKey('locality.Locality', null=True, default=None)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Corporation(SocialMediaMixin):
    """
    Information about a corporation.
    """
    name = models.CharField(max_length=255)
    address = models.ForeignKey('locality.Address', null=True, default=None)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Benefactor(models.Model):
    """
    Main list of benefactors.
    """
    benefactor_id = models.AutoField(primary_key=True)  # avoids id clash


class IndividualBenefactor(Benefactor, PersonMixin):
    """
    Individual who contributes to a committee.
    """
    occupation = models.CharField(max_length=64, null=True)


class CorporationBenefactor(Benefactor, Corporation):
    """
    Corporation that contributes to a committee.
    """
    pass


class CommitteeBenefactor(Benefactor, Committee):
    faked = models.BooleanField(default=False)
    """
    Committee that contributes to another committee, or
    spends on behalf of another committee.
    """


class Beneficiary(Committee):
    """
    Committee that receives contributions or spending
    on their behalf. The benefits must be in relation
    to a specific ballit item response.
    """
    pass


class ReportingPeriod(models.Model):
    """Model tracking form reporting periods."""
    period_start = models.DateField()
    period_end = models.DateField()


@python_2_unicode_compatible
class IndependentMoney(models.Model):
    """
    """
    support = models.BooleanField()  # Y/N
    amount = models.FloatField(help_text="Monetary value of the benefit.")
    reporting_period = models.ForeignKey('ReportingPeriod')
    benefactor_zip = models.ForeignKey('locality.ZipCode')
    benefactor = models.ForeignKey('Benefactor', help_text='Gave the benefit')
    beneficiary = models.ForeignKey('Beneficiary', help_text='Got the benefit')

    form = models.ForeignKey('Form')
    ballot_item_response = models.ForeignKey(
        'ballot.BallotItemResponse')
    filing_id = models.CharField(max_length=16)
    source = models.CharField(
        max_length=2, choices=SOURCE_TYPES, help_text="e.g. Netfile")
    source_xact_id = models.CharField(
        max_length=32, help_text="Transaction ID (specific to data source)")

    def __str__(self):
        return '%s gave %s to %s @ %s, in %s %s, reported via %s' % (
            self.benefactor, self.beneficiary, self.amount,
            self.benefactor_zip,
            'support of' if self.support else 'opposition to',
            self.ballot_item_response,
            self.form)
