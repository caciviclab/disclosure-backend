import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings

from ballot.models import Ballot, BallotItem, BallotItemResponse
from finance.models import IndependentMoney


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class FinanceTests(TestCase):

    def test_download_agencies(self, test_agency='CSA', test_year='2015'):
        """
        Tests a single file download
        """

        # Smoke test--make sure there are no errors.
        call_command('xformnetfilerawdata', verbosity=0,
                     agencies=test_agency, years=test_year)

        # Check data WESTSAC CLF STO COS
        self.assertTrue(Ballot.objects.all().count() > 0)
        self.assertTrue(BallotItem.objects.all().count() > 0)
        self.assertTrue(BallotItemResponse.objects.all().count() > 0)

        self.assertTrue(IndependentMoney.objects.all().count() > 0)
