import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings

import numpy as np

from ballot.models import Ballot, BallotItem, BallotItemSelection
from ballot.models import OfficeElection, Candidate
from ballot.models import Referendum, ReferendumSelection
from finance.models import IndependentMoney
from finance.management.commands.xformnetfilerawdata import (
    clean_city, clean_name, clean_state, clean_zip, isnan, isnone)


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class WithForm460ADataTest(TestCase):
    """
    Abstract test class for loading a netfile csv into the database.

    The default values point to a small, but relatively rich, csv.
    """
    @classmethod
    def setUpClass(cls, test_agency='CMA', test_year='2015'):
        call_command('xformnetfilerawdata',
                     agencies=test_agency, years=test_year,
                     verbosity=0)


class XformNetfileRawDataUnitTest(TestCase):
    """Unit tests on generic methods within the command file."""
    def test_isnan(self):
        """Test isnan function."""
        self.assertTrue(isnan(np.nan))
        self.assertFalse(isnan('nan'))
        self.assertFalse(isnan(''))

    def test_isnone(self):
        """Test isnone function."""
        self.assertTrue(isnone(None))
        self.assertTrue(isnone('None'))
        self.assertFalse(isnone(''))

    def test_clean_name(self):
        """Test clean_name function."""
        self.assertEqual(clean_name(None), None)
        self.assertEqual(clean_name(''), '')
        self.assertEqual(clean_name('my city'), 'My City')
        self.assertEqual(clean_name('my city, ca'), 'My City, Ca')

    def test_clean_city(self):
        """Test clean_city function."""
        self.assertEqual(clean_city(None), None)
        self.assertEqual(clean_city(''), '')
        self.assertEqual(clean_city('my city'), 'My City')
        self.assertEqual(clean_city('my city, ca'), 'My City')

    def test_clean_state(self):
        """Test clean_state function."""
        self.assertEqual(clean_state(None), None)
        self.assertEqual(clean_state(''), '')
        self.assertEqual(clean_state('my state'), 'MY STATE')

    def test_clean_zip(self):
        """Test clean_zip function."""
        self.assertEqual(clean_zip(None), None)
        self.assertEqual(clean_zip(''), '')
        self.assertEqual(clean_zip('Abc'), 'ABC')
        self.assertEqual(clean_zip('Abc 123'), 'ABC 123')
        self.assertEqual(clean_zip('12345'), '12345')
        self.assertEqual(clean_zip('12345-6789'), '12345')
        self.assertEqual(clean_zip(12345), '12345')


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class XformNetfileRawDataTest(TestCase):

    def test_xformnetfilerawdata(self, test_agency='CSA', test_year='2015',
                                 verbosity=0):
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

    def test_xformnetfilerawdata_verbose(self):
        """
        Tests a single file download, with verbosity=1
        """
        self.test_xformnetfilerawdata(verbosity=1)

    def test_xformnetfilerawdata_twice(self):
        """
        Tests a single file download, with verbosity=1
        """
        self.test_xformnetfilerawdata()
        num_rows = IndependentMoney.objects.all().count()

        self.test_xformnetfilerawdata(verbosity=1)  # print "skip"
        self.assertEqual(num_rows, IndependentMoney.objects.all().count(),
                         'no new rows after running twice')
