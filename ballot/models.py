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
    date = models.DateField(help_text='The day of the election.', null=True,
                            default=None)  # None when auto-create; manual fix
    locality = models.ForeignKey('locality.Locality')

    def __str__(self):
        return '%s election for %s' % (
            str(self.date), str(self.locality))


@python_2_unicode_compatible
class BallotItem(models.Model):
    """
    A single referendum or candidate office which appears on a voter's Ballot.
    """
    CONTEST_TYPES = (
        ('R', 'Referendum'),
        ('O', 'Office'),
    )
    contest_type = models.CharField(
        max_length=1, choices=CONTEST_TYPES,
        help_text='Office if the contest is for a person, referendum if '
                  'the contest is for an issue.')
    name = models.CharField(
        max_length=255, help_text='The referendum number or the name '
                                  'of the office.')
    number = models.CharField(
        max_length=5, null=True, default=None,
        help_text="The referendum's number or letter.")
    ballot = models.ForeignKey('Ballot')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BallotItemResponse(models.Model):
    """
    YES/NO to a referendum, or a candidate.
    """
    # None indicates auto-set and needs manual intervention.
    title = models.CharField(max_length=255)
    brief = models.TextField(null=True, blank=True, default=None)
    full_text = models.TextField(null=True, blank=True, default=None)
    pro_statement = models.TextField(null=True, blank=True, default=None)
    con_statement = models.TextField(null=True, blank=True, default=None)
    ballot_item = models.ForeignKey('BallotItem')

    def __str__(self):
        return "%s on %s" % (self.title, self.ballot_item.name)