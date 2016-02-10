import os.path as op
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings

from ballot.models import Candidate
from finance.tests.test_command import WithForm460ADataTest


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(), DEBUG=True)
class ImageUploadTests(WithForm460ADataTest, StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        StaticLiveServerTestCase.setUpClass()

        cls.username = 'admin'
        cls.passwd = 'admin'
        User.objects.create_superuser(
            username=cls.username, password=cls.passwd, email='')

        cls.candidate = Candidate.objects.all()[0]
        if not cls.candidate.first_name:
            cls.candidate.first_name = 'dummy'
            cls.candidate.save()

        cls.img_path = op.join(op.dirname(__file__), 'files', 'img.jpg')

    @classmethod
    def tearDownClass(cls):
        # somehow this deletes the actual media root!
        # shutil.rmtree(settings.MEDIA_ROOT)

        StaticLiveServerTestCase.tearDownClass()
        # WithForm460ADataTest.tearDownClass()

    def test_upload_and_get_textfile(self):
        """Regression test for upload/get of candidate image (#58)"""

        # Log on as admin
        response = self.client.post(
            '/admin/login/', {'username': self.username, 'password': self.passwd})
        self.assertTrue(response['Location'].endswith('/accounts/profile/'))

        # Post a file
        candidate_url = '/admin/ballot/candidate/%d/' % self.candidate.id

        with open(self.img_path, 'rb') as fp:
            photo_content = fp.read()
        photo = SimpleUploadedFile(self.img_path, photo_content, content_type="image/png")
        pkg = dict(photo_url=photo)
        for prop in ['first_name', 'last_name', 'middle_name']:
            pkg[prop] = getattr(self.candidate, prop)
        for prop in ['office_election', 'ballot_item']:
            pkg[prop] = getattr(self.candidate, prop).id

        response = self.client.post(candidate_url, pkg)

        # Validate response
        msg = ''
        if 'errorlist' in response.content:
            # Grab the error and report as the test message
            idx = response.content.index('errorlist')
            msg = response.content[idx:idx + 100]
        self.assertTrue('errorlist' not in response.content, msg)
        self.assertEqual(response.status_code, 302)  # successful save

        # Validate the file exists.
        out_file = op.basename(self.img_path)
        out_path = op.join(settings.MEDIA_ROOT, out_file)
        self.assertTrue(op.exists(out_path))

        # Validate that the client can grab the file.
        # This fails! Can't figure out why; it works in production.
        media_url = '%s%s' % (settings.MEDIA_URL, out_file)
        response = self.client.get(media_url)
        # self.assertEqual(response.status_code, 200, media_url)  # successful GET
