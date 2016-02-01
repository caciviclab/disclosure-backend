import os.path as op
import tempfile
import warnings

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings

from netfile_raw import connect2_api
from netfile_raw.models import NetFileAgency, NetFileCal201Transaction


@override_settings(NETFILE_DOWNLOAD_DIR=tempfile.mkdtemp())
class NetfileTests(TestCase):
    def test_models_import_correctly(self):
        """
        Tests that the modules can be imported, (that's something).
        """
        self.assertIsNotNone(connect2_api)

    def test_combine_agencies_without_download(self, test_agency='CPA',
                                               test_year='2015'):

        call_command('downloadnetfilerawdata',
                     skip_combine=True, skip_load=True, agencies=test_agency,
                     years=test_year)

        call_command('downloadnetfilerawdata',
                     skip_download=True, skip_load=True, agencies=test_agency,
                     years=test_year)

    def test_download_agencies(self, test_agency='CPA', test_year='2015'):
        """
        Tests a single file download
        """

        # Smoke test--make sure there are no errors.
        call_command('downloadnetfilerawdata',
                     agencies=test_agency, years=test_year)

        agencies_path = op.join(settings.NETFILE_DOWNLOAD_DIR,
                                'csv', 'netfile_agency.csv')
        self.assertTrue(op.exists(agencies_path), agencies_path)

        data_path = op.join(settings.NETFILE_DOWNLOAD_DIR,
                            'csv', 'netfile_%s_%s_cal201_export.csv' % (
                                test_year, test_agency))
        self.assertTrue(op.exists(data_path), data_path)

        # Check data
        self.assertTrue(NetFileCal201Transaction.objects.all().count() > 0)
        self.assertTrue(NetFileAgency.objects.all().count() > 0)

    def test_download_warnings(self):
        """
        """

        # Make sure warning occurs.
        with warnings.catch_warnings():
            warnings.simplefilter("error")

            # Bad agency
            self.assertRaises(
                Warning, call_command, 'downloadnetfilerawdata',
                agencies='XXX', years='2015')

            # Bad year
            self.assertRaises(
                Warning, call_command, 'downloadnetfilerawdata',
                agencies='CSD', years='1900')

    def test_download_warnings_ignored(self):
        """
        """

        # Make sure the command completes.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Bad agency
            call_command('downloadnetfilerawdata',
                         agencies='XXX', years='2015')
            self.assertEqual(NetFileCal201Transaction.objects.all().count(), 0)

            # Bad year
            call_command('downloadnetfilerawdata',
                         agencies='CSD', years='1900')
            self.assertEqual(NetFileCal201Transaction.objects.all().count(), 0)
