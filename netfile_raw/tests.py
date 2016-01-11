import os.path as op
import tempfile

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
