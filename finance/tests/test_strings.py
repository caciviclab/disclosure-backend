from django.test import TestCase

from .utils import with_form460A_data
from finance.models import (IndependentMoney, Beneficiary, CommitteeBenefactor,
                            OtherBenefactor, PersonBenefactor, PartyBenefactor,
                            Benefactor, Committee)


@with_form460A_data
class IndependentMoneyStringTests(TestCase):

    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """

        for cls in [IndependentMoney, Beneficiary, CommitteeBenefactor,
                    OtherBenefactor, PersonBenefactor, Benefactor,
                    PartyBenefactor, Committee]:
            if cls.objects.all().count() == 0:  # bad :(
                try:
                    obj = cls()
                except:
                    continue
            else:
                obj = cls.objects.all()[0]

            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)
