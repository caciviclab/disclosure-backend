from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ballot_measure.models import BallotItemChoice


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
        max_length=255, help_text='The candidate\'s first name.')
    middle_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='The candidate\'s middle name.')
    last_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='The candidate\'s last name.')
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
            self.name, self.locality.dereference())


@python_2_unicode_compatible
class Election(models.Model):
    """
    """
    office = models.ForeignKey('Office')
    ballot_measure = models.ForeignKey(
        'ballot_measure.BallotItem')

    def locality(self):
        return self.ballot_measure.ballot.locality

    def __str__(self):
        return "Election of %s in %s" % (
            self.office.name, self.locality().dereference())


class Candidate(BallotItemChoice, SocialMediaModel):
    """
    A person running for office.
    """
    person = models.ForeignKey('Person')
    election = models.ForeignKey('Election')

    # Should alias biography = models.TextField(blank=True)

    def __str__(self):
        return self.name
