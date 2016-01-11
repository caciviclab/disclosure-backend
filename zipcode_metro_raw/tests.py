import os.path as op
import tempfile

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings

from zipcode_metro_raw.models import ZipCodeMetro


@override_settings(CALACCESS_DOWNLOAD_DIR=tempfile.mkdtemp())
class ZipcodeMetroTest(TestCase):

    def test_download_agencies(self):
        """
        Tests a single file download
        """

        # Smoke test--make sure there are no errors.
        call_command('downloadzipcodedata')

        zipcodes_path = op.join(settings.CALACCESS_DOWNLOAD_DIR,
                                'csv', 'zipcode_metro.csv')
        self.assertTrue(op.exists(zipcodes_path), zipcodes_path)

        # Check data
        self.assertTrue(ZipCodeMetro.objects.all().count() > 0)
