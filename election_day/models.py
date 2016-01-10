from django.db import models


class ElectionDay(models.Model):
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
    ballot = models.ForeignKey('ballot.Ballot')
