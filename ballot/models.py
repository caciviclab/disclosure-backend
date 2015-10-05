"""
Ballot related models. Everything a voter needs to vote on.
Models are influenced from http://votinginfoproject.github.io/vip-specification/
"""
from django.db import models

class Election(models.Model):
    """
    A single election day.
    """
    ELECTION_TYPES = (
        ('FE', 'Federal'),
        ('ST', 'State'),
        ('CO', 'County'),
        ('CI', 'City'),
    )
    date = models.DateField(help_text='The day of the election.')
    election_type = models.CharField(
        max_length=2,
        choices=ELECTION_TYPES,
        help_text='''
        Specifies the highest controlling authority for the election
        (e.g., federal, state, county, city, town, etc.)
        '''
    )


class Locality(models.Model):
    """
    Represents a jurisdiction under the state level, could be county or city.
    """
    LOCALITY_TYPES = (
        ('CO', 'County'),
        ('CI', 'City'),
        #TODO but maybe other things (township, borough, region, etc.)
    )
    name = models.CharField(max_length=255, help_text='Name of the juristiction.')
    locality_type = models.CharField(
        max_length=2,
        choices=LOCALITY_TYPES,
        help_text='One of county, city, township, borough, parish, village, or region.'
    )
    #TODO Make this a proper foreign key to netfile agency
    netfile_agency = models.CharField(
        max_length=10,
        help_text='The netfile agency administering the elections in this locality.'
    )


class Ballot(models.Model):
    """
    A voter's ballot, containing all the BallotItems that the voter will vote
    on in the voting booth on election day.
    """
    election = models.ForeignKey('Election')
    locality = models.ForeignKey('Locality')


class Contest(models.Model):
    """
    A single referendum or candidate office which appears on a voter's Ballot.
    """
    CONTEST_TYPES = (
        ('R', 'Referendum'),
        ('O', 'Office'),
    )
    ballot = models.ForeignKey('Ballot')
    contest_type = models.CharField(
        max_length=1,
        help_text='''
        Office if the contest is for a person, referendum if the contest is for an issue.
        '''
    )


class Precinct(models.Model):
    """
    The smallest unit of geographic area for voters. Your precinct determines
    who and what you vote on.
    """
    name = models.CharField(max_length=30, help_text="The precinct's name or number.")
    number = models.CharField(
        max_length=5,
        help_text="the precinct's number e.g., 32 or 32A (alpha characters are legal)."
    )
    locality = models.ForeignKey('Locality')


class Candidate(models.Model):
    """
    A person running for office.
    """
    contest = models.ForeignKey('Contest')
    name = models.CharField(max_length=255, help_text='The candidate\'s full name.')
    biography = models.TextField()
    photo_url = models.ImageField()
    candidate_url = models.URLField(help_text='URL for the candidate\'s official website.')
    facebook_url = models.URLField(help_text='URL for the candidate\'s Facebook page.')
    twitter_url = models.URLField(help_text='URL for the candidate\'s Twitter page.')


class Referendum(models.Model):
    """
    A ballot measure, proposition, or referendum.
    """
    contest = models.ForeignKey('Contest')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    brief = models.TextField()
    full_text = models.TextField()
    pro_statement = models.TextField()
    con_statement = models.TextField()
