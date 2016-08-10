from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase


class TestServerSetupTest(TestCase):

    def test_setup_test_server(self):
        """ Test setuptestserver"""
        call_command('setuptestserver')
        # Didn't throw; check some minimum level of output.
        self.assertTrue(User.objects.get(username="admin").username, "admin")
