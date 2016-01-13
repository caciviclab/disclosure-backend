"""
Models representing the election event.
"""

from django.db import models


class ElectionDay(models.Model):
    """
    A single election day.
    """
    ballot = models.ForeignKey('ballot.Ballot')
