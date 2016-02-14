"""
Models related to elections for a specific office
in a specific locality.
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .ballot import BallotItem, BallotItemSelection


class SocialMediaMixin(models.Model):
    """
    Abstract class to represent social media information.
    """
    photo_url = models.ImageField(blank=True, null=True, default=None)
    website_url = models.URLField(blank=True, null=True, default=None)
    facebook_url = models.URLField(blank=True, null=True, default=None)
    twitter_url = models.URLField(blank=True, null=True, default=None)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Party(SocialMediaMixin):
    """
    Political party
    """
    name = models.CharField(
        max_length=255, help_text='The party name.')

    def __str__(self):
        return "The %s party" % self.name

    class Meta:
        verbose_name_plural = 'parties'
        ordering = ('name',)


@python_2_unicode_compatible
class PersonMixin(SocialMediaMixin):
    """
    Abstract class representing a person.
    """
    first_name = models.CharField(max_length=255, null=True, default=None,
                                  help_text="The person's first name.")
    middle_name = models.CharField(max_length=255, blank=True,
                                   null=True, default=None,
                                   help_text="The person's middle name.")
    last_name = models.CharField(max_length=255,
                                 help_text="The person's last name.")

    def __str__(self):
        name = self.last_name
        if self.first_name:
            name += ", %s" % self.first_name
            if self.middle_name:
                name += " %s." % self.middle_name[0]
        return name

    class Meta:
        abstract = True
        ordering = ('last_name', 'first_name', 'middle_name')


@python_2_unicode_compatible
class Office(models.Model):
    """
    A political office in a specific locality.
    """
    name = models.CharField(
        max_length=255, help_text='The office name.')
    description = models.CharField(
        max_length=1024, help_text='The office description.')
    locality = models.ForeignKey('locality.Locality')

    def __str__(self):
        return "Office for %s in %s" % (
            self.name, str(self.locality))

    class Meta:
        ordering = ('locality__short_name', 'locality__name',
                    'name')


@python_2_unicode_compatible
class OfficeElection(BallotItem):
    """
    A specific ballot item to elect a candidate to an office.
    """
    office = models.ForeignKey('Office')

    def __init__(self, *args, **kwargs):
        super(OfficeElection, self).__init__(*args, **kwargs)
        self.contest_type = 'O'

    def __str__(self):
        return "Election of %s in %s (on %s)" % (
            self.office.name, str(self.office.locality),
            self.ballot.date)

    class Meta:
        ordering = BallotItem._meta.ordering + ('office__name',)


@python_2_unicode_compatible
class Candidate(BallotItemSelection, PersonMixin):
    """
    A person running for office.
    """
    office_election = models.ForeignKey('OfficeElection')
    party = models.ForeignKey('Party', blank=True, null=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)
        has_ballot_item = getattr(self, 'ballot_item', None) is not None
        has_office_election = getattr(self, 'office_election', None) is not None

        if has_ballot_item and has_office_election:
            assert self.ballot_item.id == self.office_election.id
        elif has_ballot_item:
            self.office_election = self.ballot_item
        elif has_office_election:
            self.ballot_item = self.office_election

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return "%s for %s" % (  # use unicode to avoid recursion error
            PersonMixin.__unicode__(self), self.office_election)

    class Meta:
        ordering = (BallotItemSelection._meta.ordering +
                    ('office_election__office__name',) +
                    PersonMixin._meta.ordering)
