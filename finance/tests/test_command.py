import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings

from ballot.models import Ballot, BallotItem, BallotItemSelection
from ballot.models import OfficeElection, Candidate
from ballot.models import Referendum, ReferendumSelection
from finance.models import IndependentMoney


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class WithForm460ADataTest(TestCase):
    """
    """
    @classmethod
    def setUpClass(cls, test_agency='CMA', test_year='2015'):
        call_command('xformnetfilerawdata',
                     agencies=test_agency, years=test_year,
                     verobsity=0)


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class XformNetfileRawDataTest(TestCase):

    def test_xformnetfilerawdata(self, test_agency='CSA', test_year='2015'):
        """
        Tests a single file download
        """

        # Smoke test--make sure there are no errors.
        call_command('xformnetfilerawdata', verbosity=0,
                     agencies=test_agency, years=test_year)

        # Check data
        for model in [Ballot, BallotItem, BallotItemSelection,
                      Referendum, ReferendumSelection,
                      OfficeElection, Candidate,
                      IndependentMoney]:

            self.assertTrue(model.objects.all().count() > 0,
                            '%ss exist after parse' % model.__class__.__name__)
