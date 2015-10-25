from rest_framework.test import APITestCase
from calaccess_raw.models.campaign import RcptCd
from django.core.management import call_command


class ContributionTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()
        call_command(
            'downloadcalaccessrawdata',
            verbosity=1,
            test_data=True
        )

    def test_list_contains_data(self):
        resp = self.client.get('/contributions/')
        self.assertGreater(len(resp.data), 0)
        row = resp.data[0]
        self.assertIn('amount', row)

    def test_retrieve_contains_data(self):
        first_contribution_id = RcptCd.objects.all()[0].id
        resp = self.client.get('/contributions/{0}/'.format(first_contribution_id))
        self.assertIn('amount', resp.data)
