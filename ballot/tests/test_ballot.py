from django.test import TestCase

from ballot.models import Ballot


class ObjectCreateTest(TestCase):
    def test_create_empty(self):
        ballot = Ballot()  # noqa
