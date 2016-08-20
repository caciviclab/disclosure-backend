from django.test import TestCase

from finance.tests.utils import with_form460A_data
from ballot.models import (Ballot, BallotItem, BallotItemSelection,
                           Party)


@with_form460A_data
class BallotStringTests(TestCase):

    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """

        for cls in [Ballot, BallotItem, BallotItemSelection, Party]:
            if cls.objects.all().count() == 0:  # bad :(
                continue
            obj = cls.objects.all()[0]
            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)
