"""
Ballot related models. Everything a voter needs to vote on.
Models are influenced from
http://votinginfoproject.github.io/vip-specification/
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

    def __str__(self):
        return str(self.date)

    def __unicode__(self):
        return unicode(self.date)


class Ballot(models.Model):
    """
    A voter's ballot, containing all the BallotItems that the voter will vote
    on in the voting booth on election day.
    """
    election = models.ForeignKey('Election')
    locality = models.ForeignKey('locality.Locality')

    def __str__(self):
        return '%s election for %s' % (
            str(self.election.date), self.locality.name)

    def __unicode__(self):
        return '%s election for %s' % (
            str(self.election.date), self.locality.name)


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
        choices=CONTEST_TYPES,
        help_text='Office if the contest is for a person, referendum if '
                  'the contest is for an issue.'
    )
    name = models.CharField(
        max_length=255, help_text='The referendum number or the name '
                                  'of the office.')

    def __str__(self):
        prefix = ''
        if self.contest_type is 'R':
            prefix = 'Prop '

        return '%s%s' % (prefix, self.name)

    def __unicode__(self):
        prefix = ''
        if self.contest_type is 'R':
            prefix = 'Prop '

        return '%s%s' % (prefix, self.name)

    class Meta:
        verbose_name = 'race'


class Referendum(models.Model):
    """
    A ballot measure, proposition, or referendum.
    """
    contest = models.ForeignKey('Contest', blank=True, null=True)
    number = models.CharField(
        max_length=5, help_text="The referendum's number or letter.")
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    brief = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    pro_statement = models.TextField(blank=True)
    con_statement = models.TextField(blank=True)

    def __str__(self):
        return 'Prop %s %s' % (self.number, self.title)

    def __unicode__(self):
        return 'Prop %s %s' % (self.number, self.title)

    class Meta:
        verbose_name = 'ballot measure'
