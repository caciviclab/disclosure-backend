from django.test import TestCase

from locality.models import City, State, County


class LocalityStringTest(TestCase):
    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """

        state, _ = State.objects.get_or_create(name='California')
        city, _ = City.objects.get_or_create(name='San Diego', state=state)
        county, _ = County.objects.get_or_create(name='San Diego', state=state)

        for obj in [state, city, county]:
            cls = obj.__class__
            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)
