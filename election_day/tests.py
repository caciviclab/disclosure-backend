from django.test import TestCase

from rest_framework.test import APITestCase

from election_day.models import ElectionDay
from locality.models import City, State
from ballot.models import Ballot, Office


class ElectionDayTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ElectionDayTest, cls).setUpClass()
        state, _ = State.objects.get_or_create(name='California')
        city, _ = City.objects.get_or_create(name='San Diego', state=state)
        office, _ = Office.objects.get_or_create(name='Mayor', locality=city)
        ballot, _ = Ballot.objects.get_or_create(locality=city)
        cls.election_day, _ = ElectionDay.objects.get_or_create(ballot=ballot)


class ElectionDayStringTest(ElectionDayTest):
    def test_election_day_str(self):
        obj = self.election_day
        cls = obj.__class__
        self.assertNotIn('Object', str(obj), cls.__name__)
        self.assertNotIn('Object', unicode(obj), cls.__name__)

        self.assertNotEqual('', str(obj), cls.__name__)
        self.assertNotEqual('', unicode(obj), cls.__name__)


class ElectionDayAPITest(ElectionDayTest, APITestCase):
    @classmethod
    def setUpClass(cls):
        ElectionDayTest.setUpClass()
        APITestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        ElectionDayTest.tearDownClass()
        APITestCase.tearDownClass()

    def test_election_day_api(self):
        """
        Access election day object through the API.
        """
        resp = self.client.get('/elections/')
        self.assertEqual(resp.status_code, 200)

        # TODO: flesh out test when data are live/available for this app.
