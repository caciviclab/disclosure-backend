"""
Models related to elections for a specific office
in a specific locality.
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ballot.models import BallotItem, BallotItemSelection


class SocialMediaMixin(models.Model):
    """
    Abstract class to represent social media information.
    """
    photo_url = models.ImageField(null=True, default=None)
    website_url = models.URLField(null=True, default=None)
    facebook_url = models.URLField(null=True, default=None)
    twitter_url = models.URLField(null=True, default=None)

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


@python_2_unicode_compatible
class PersonMixin(SocialMediaMixin):
    """
    Abstract class representing a person.
    """
    first_name = models.CharField(max_length=255, null=True, default=None,
                                  help_text="The person's first name.")
    middle_name = models.CharField(max_length=255, null=True, default=None,
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


@python_2_unicode_compatible
class OfficeElection(BallotItem):
    """
    A specific ballot item to elect a candidate to an office.
    """
    office = models.ForeignKey('Office')

    def __init__(self, *args, **kwargs):
        super(OfficeElection, self).__init__(*args, **kwargs)
        self.contest_type = 'O'
        # set BallotItem fields from Office
        self.name = str(self)

    def __str__(self):
        return "Election of %s in %s" % (
            self.office.name, str(self.office.locality))


@python_2_unicode_compatible
class Candidate(BallotItemSelection, PersonMixin):
    """
    A person running for office.
    """
    office_election = models.ForeignKey('OfficeElection')
    party = models.ForeignKey('Party', null=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)
        if getattr(self, 'ballot_item', None) is None:
            self.ballot_item = self.office_election
        elif getattr(self, 'office_election', None) is None:
            self.office_election = self.ballot_item
        else:
            assert self.ballot_item.id == self.office_election.id

    def __str__(self):
        return "%s for %s" % (  # use unicode to avoid recursion error
            PersonMixin.__unicode__(self), self.office_election)
