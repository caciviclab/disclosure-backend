from rest_framework.test import APITestCase


class ApiDocsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        APITestCase.setUpClass()

    def test_docs(self):
        self.client.get('/docs/')  # smoke test

    def test_api_docs(self):
        resp = self.client.get('/docs/api-docs/')
        self.assertIn('apis', resp.data)
