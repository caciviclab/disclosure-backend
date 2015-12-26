import os
from django.conf import settings
from django.core.management import call_command
from rest_framework.test import APITestCase


class DocGenerationTest(APITestCase):

    def test_generate_docs(self):
        """ Test createcalaccessrawmodeldocs"""
        call_command('createcalaccessrawmodeldocs')
        # Didn't throw; check some minimum level of output.
        docs_dir = os.path.join(settings.REPO_DIR, 'docs')
        self.assertTrue(os.path.exists(docs_dir))
