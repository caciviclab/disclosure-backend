from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from office_election.models import SocialMediaMixin, PersonMixin


@python_2_unicode_compatible
class Committee(SocialMediaMixin):
    COMMITTEE_TYPES = (
        ('OF', 'Primarily-formed Official Committee'),
        ('PF', 'Primariliy-formed Committee'),
        ('IC', 'Independent Committee')
    )
    name = models.CharField(max_length=255)
    address = models.ForeignKey('locality.Address', null=True)
    locality = models.ForeignKey('locality.Locality', null=True)
    filer_id = models.CharField(max_length=16, unique=True)
    type = models.CharField(
        max_length=2,
        choices=COMMITTEE_TYPES,
        help_text=''
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Corporation(SocialMediaMixin):
    name = models.CharField(max_length=255)
    address = models.ForeignKey('locality.Address', null=True)
    # locality = models.ForeignKey('locality.Locality', null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Form(models.Model):
    """
    """
    name = models.CharField(max_length=255)
    text_id = models.CharField(
        max_length=32, help_text='e.g. 460 Schedule A')
    FREQUENCY_TYPES = (
        ('24', '24 hours'),
        ('SA', 'Semi-annual'),
        ('QU', 'Quarterly'),
        ('OT', 'Other')
    )
    submission_frequency = models.CharField(
        max_length=2,
        choices=FREQUENCY_TYPES,
        help_text=''
    )

    def dereference(self):
        pass

    def __str__(self):
        return self.name


class Benefactor(models.Model):
    """  # noqa
    Skipping: tran_Adr1
    Skipping: tran_Adr2
    tran_Amt1      : Transaction Amount, 3000.0,12032.56,5000.0,4950.0,
    tran_Amt2      : Cumulative Year-To-Date, 15032.56,5000.0,4950.0,100.0,1
    Skipping: tran_ChkNo
    tran_City      : Transaction Entity's City, San Diego,Sacramento,Los Angel
    Skipping: tran_Code
    tran_Date      : Transaction Date, 2015-01-15T00:00:00.0000000-08
    Skipping: tran_Date1
    tran_Dscr      : Transaction Description, nan,Forgiven Loan Received,Con
    tran_Emp       : Transaction Entity's Employer, nan,retired,Retired,Self emplo
    tran_Id        : Transaction ID # (not necessar, A-C702,A-C706,A37,A40,gYfv3kGK
    tran_NamF      : Transaction Entity's First Nam, Mitz S.,nan,Marie,Barbara,Stev
    tran_NamL      : Transaction Entity's Last Name, Lee,California Restaurant Asso
    tran_NamS      : Transaction Entity's Suffix, nan,Jr,Sr,Jr.,III,MD,IV,II,`,D
    tran_NamT      : Transaction Entity's Prefix or, nan,Mr.,Ms.,Dr.
    tran_Occ       : Transaction Entity's Occupatio, City Council Candidate,nan,ret
    tran_ST        : None, CA,NY,AZ,CO,TX,FL,AE,IL,KS,VA,
    Skipping: tran_Self
    tran_Type      : Transaction Type (T=Third Part, nan,I,F,R
    tran_Zip4      : Transaction Entity's Zip Code, 92126-1531,95814,92119,92115,9
    """
    benefactor_id = models.AutoField(primary_key=True)  # avoids id clash

    def dereference(self):
        for rel in self._meta.get_all_related_objects():
            if hasattr(self, rel.name):
                return getattr(self, rel.name)
        raise Exception("Abstract benefactor? %s" % self)


class IndividualBenefactor(Benefactor, PersonMixin):
    occupation = models.CharField(max_length=64, null=True)


class CorporationBenefactor(Benefactor, Corporation):
    pass


class CommitteeBenefactor(Benefactor, Committee):
    faked = models.BooleanField(default=False)


class Beneficiary(Committee):
    pass


class ReportingPeriod(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()


@python_2_unicode_compatible
class IndependentMoney(models.Model):
    """
    """
    amount = models.FloatField()
    support = models.BooleanField()  # Y/N
    benefactor_zip = models.ForeignKey('locality.ZipCode')

    form = models.ForeignKey('Form')
    reporting_period = models.ForeignKey('ReportingPeriod')
    benefactor = models.ForeignKey(
        'Benefactor', help_text='They gave the money')
    beneficiary = models.ForeignKey(
        'Beneficiary', help_text='They got the money')
    ballot_item_response = models.ForeignKey(
        'ballot.BallotItemResponse')
    filing_id = models.CharField(max_length=16)
    source = models.CharField(max_length=2)
    source_xact_id = models.CharField(max_length=32)

    def __str__(self):
        return '%s gave %s to %s @ %s, in %s %s, reported via %s' % (
            self.benefactor, self.beneficiary, self.amount,
            self.benefactor_zip,
            'support of' if self.support else 'opposition to',
            self.ballot_item_response,
            self.form)
