from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework.test import APITestCase

from locality.models import City, State, County


class LocalityTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LocalityTest, cls).setUpClass()
        cls.state, _ = State.objects.get_or_create(name='California')
        cls.city, _ = City.objects.get_or_create(name='San Diego', state=cls.state)
        cls.county, _ = County.objects.get_or_create(name='San Diego', state=cls.state)


class LocalityAPITests(LocalityTest, APITestCase):
    @classmethod
    def setUpClass(cls):
        LocalityTest.setUpClass()
        APITestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        LocalityTest.tearDownClass()
        APITestCase.tearDownClass()

    def test_docs(self):
        locality_url = reverse('locality_get', kwargs={'locality_id': self.city.id})
        resp = self.client.get(locality_url)

        self.assertIn('name', resp.data)
        self.assertIn('id', resp.data)


class LocalityStringTest(LocalityTest):
    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """
        for obj in [self.state, self.city, self.county]:
            cls = obj.__class__
            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)
