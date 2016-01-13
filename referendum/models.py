"""
Models related to a specific referendum on a ballot.
"""

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from ballot.models import BallotItem
from office_election.models import SocialMediaMixin


@python_2_unicode_compatible
class Referendum(BallotItem, SocialMediaMixin):
    """
    A referendum on the ballot.
    """
    # TODO: Set up a save() event, or overload save(), to auto-populate
    #   BallotItemResponses (YES/NO)

    def __init__(self, *args, **kwargs):
        super(Referendum, self).__init__(*args, **kwargs)
        self.contest_type = 'R'

    def __str__(self):
        return "Prop %s: %s" % (self.number, self.name)
