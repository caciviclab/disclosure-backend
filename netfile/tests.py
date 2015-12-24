from django.test import TestCase

# from . import models
from . import connect2_api


class NetfileTests(TestCase):

    def test_models_import_correctly(self):
        """
        Tests that the modules can be imported, (that's something).
        """
        self.assertIsNotNone(connect2_api)
