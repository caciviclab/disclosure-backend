"""
Ballot related models. Everything a voter needs to vote on.
Models are influenced from
http://votinginfoproject.github.io/vip-specification/
"""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Ballot(models.Model):
    """
    A voter's ballot, containing all the BallotItems that the voter will vote
    on in the voting booth on election day.
    """
    date = models.DateField(help_text='The day of the election.',
                            null=True, default=None)
    locality = models.ForeignKey('locality.Locality')

    def __str__(self):
        return '%s election for %s' % (
            str(self.date), str(self.locality))


@python_2_unicode_compatible
class BallotMeasure(models.Model):
    """
    A single referendum or candidate office which appears on a voter's Ballot.
    """
    CONTEST_TYPES = (
        ('R', 'Referendum'),
        ('O', 'Office'),
    )
    contest_type = models.CharField(
        max_length=1,
        choices=CONTEST_TYPES,
        help_text='Office if the contest is for a person, referendum if '
                  'the contest is for an issue.'
    )
    name = models.CharField(
        max_length=255, help_text='The referendum number or the name '
                                  'of the office.')
    number = models.CharField(
        max_length=5, help_text="The referendum's number or letter.")

    ballot = models.ForeignKey('Ballot')

    def __str__(self):
        return 'Prop %s %s' % (self.number, self.title)

    class Meta:
        verbose_name = 'ballot measure'


@python_2_unicode_compatible
class BallotMeasureChoice(models.Model):
    ballot_measure = models.ForeignKey('BallotMeasure')

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    brief = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    pro_statement = models.TextField(blank=True)
    con_statement = models.TextField(blank=True)

    def __str__(self):
        return 'Option: %s%s' % (self.title, self.subtitle)
