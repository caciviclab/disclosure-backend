from __future__ import unicode_literals

from ballot.models import BallotItem
from office_election.models import SocialMediaMixin


class Referendum(BallotItem, SocialMediaMixin):
    """
    A referendum on the ballot. Can be YES/NO or multiple choice.
    """
    # TODO: Set up a save() event, or overload save(), to auto-populate
    #   BallotItemResponses (YES/NO)

    def __init__(self, *args, **kwargs):
        super(Referendum, self).__init__(*args, **kwargs)
        self.contest_type = 'R'
