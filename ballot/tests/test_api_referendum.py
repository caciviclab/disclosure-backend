from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class MeasureAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_referendum_with_id(self):
        resp = self.client.get(reverse('referendum_get', kwargs={'referendum_id': 1}))

        self.assertIn('id', resp.data)
        self.assertIn('name', resp.data)
        self.assertIn('number', resp.data)
