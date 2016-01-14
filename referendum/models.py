"""
Models related to a specific referendum on a ballot.
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ballot.models import BallotItem, BallotItemResponse
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


@python_2_unicode_compatible
class ReferendumResponse(BallotItemResponse, SocialMediaMixin):
    """
    A referendum response on the ballot (usually YES or NO)
    """
    # None indicates auto-set and needs manual intervention.
    in_favor = models.NullBooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return "'%s' on %s" % (
            "FOR" if self.in_favor else "OPPOSED", self.ballot_item.name)
