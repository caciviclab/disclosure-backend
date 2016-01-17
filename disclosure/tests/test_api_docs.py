from rest_framework.test import APITestCase


class ApiDocsTests(APITestCase):
    ALL_API_PATHS = ['/ballot', '/committee', '/contributions',
                     '/contributors', '/elections', '/locations',
                     '/measure', '/opposing', '/search',
                     '/supporting']

    @classmethod
    def setUpClass(cls):
        APITestCase.setUpClass()

    def test_list_contains_data(self):
        resp = self.client.get('/docs/api-docs')
        self.assertIn('apis', resp.data)

        for api in resp.data['apis']:
            self.assertIn(api['path'], self.ALL_API_PATHS, api['path'])
