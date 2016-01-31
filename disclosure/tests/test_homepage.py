from tempfile import mkdtemp
import os
import shutil

from django.test import TestCase
from django.test.utils import override_settings


class HomepageTest(TestCase):

    @override_settings(CRON_LOGS_DIR=None)
    def test_works_without_cron_logs_dir(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Cron Status')


    def test_works_with_cron_logs_dir(self):
        cron_dir = None

        try:
            cron_dir = mkdtemp()
            fake_cron_log = "Foo bar baz\n"

            # create a fake cron log
            with open(os.path.join(cron_dir, 'cron_log.out'), 'w') as f:
                f.write(fake_cron_log)

            with self.settings(CRON_LOGS_DIR=cron_dir):
                response = self.client.get('/')
                self.assertContains(response, 'Cron Status')
                self.assertContains(response, fake_cron_log)

        finally:
            if cron_dir:
                shutil.rmtree(cron_dir)
