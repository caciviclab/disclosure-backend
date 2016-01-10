from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ballot.models import BallotItem, BallotItemResponse


class SocialMediaModel(models.Model):
    class Meta:
        abstract = True

    photo_url = models.ImageField(blank=True)
    website_url = models.URLField(
        help_text='URL for the official website.', blank=True)
    facebook_url = models.URLField(
        help_text='URL for the Facebook page.', blank=True)
    twitter_url = models.URLField(
        help_text='URL for the Twitter page.', blank=True)


@python_2_unicode_compatible
class Party(SocialMediaModel):
    """
    """
    name = models.CharField(
        max_length=255, help_text='The party name.')

    def __str__(self):
        return "The %s party" % self.name


@python_2_unicode_compatible
class Person(SocialMediaModel):
    """
    """
    first_name = models.CharField(
        max_length=255, help_text="The person's first name.")
    middle_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="The person's middle name.")
    last_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="The person's last name.")
    party = models.ForeignKey('Party', blank=True, null=True)

    def __str__(self):
        return "%s, %s%s" % (
            self.last_name, self.first_name,
            '' if self.middle_name is None else ' %s.' % self.middle_name[0])


@python_2_unicode_compatible
class Office(models.Model):
    """
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
class Candidate(BallotItemResponse, SocialMediaModel):
    """
    A person running for office.
    """
    person = models.ForeignKey('Person')
    office_election = models.ForeignKey('OfficeElection')

    def __init__(self, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)
        # set BallotItemResponse fields from Person, Office
        self.title = str(self.person)
        self.subtitle = str(self.office_election)
        self.ballot_item = self.office_election

    def __init__(self, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)
        self.title = str(self.person)
        self.subtitle = str(self.office_election)

    def __str__(self):
        return self.title
