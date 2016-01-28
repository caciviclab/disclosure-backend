import glob
import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase


class DocGenerationTest(TestCase):
    docs_dir = os.path.join(settings.REPO_DIR, 'docs')

    def test_generate_calaccess_model_docs(self):
        """ Test createcalaccessrawmodeldocs"""
        call_command('createcalaccessrawmodeldocs')
        # Didn't throw; check some minimum level of output.
        self.assertTrue(os.path.exists(self.docs_dir))

    def test_create_er(self):
        call_command('generate_project_er_diagram')
        self.assertTrue(os.path.exists(self.docs_dir))

        png_files = glob.glob(os.path.join(self.docs_dir, 'model-*.png'))
        self.assertEqual(len(png_files), 2)
