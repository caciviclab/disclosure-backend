from rest_framework.test import APITestCase

from finance.tests.test_command import WithForm460ADataTest


class MeasureAPITests(WithForm460ADataTest, APITestCase):

    @classmethod
    def setUpClass(cls):
        # WithForm460ADataTest.setUpClass()
        APITestCase.setUpClass()

    def test_measure_with_id(self):
        resp = self.client.get('/measure/%d' % 1)

        self.assertIn('measure_id', resp.data)
        self.assertIn('city', resp.data)
