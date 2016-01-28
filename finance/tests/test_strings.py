from django.test import TestCase

from .test_command import WithForm460ADataTest
from finance.models import (IndependentMoney, Beneficiary, CommitteeBenefactor,
                            CorporationBenefactor, PersonBenefactor,
                            Benefactor, Form, Committee)


class IndependentMoneyStringTests(WithForm460ADataTest, TestCase):

    @classmethod
    def setUpClass(cls):
        TestCase.setUpClass()
        WithForm460ADataTest.setUpClass()

    def test_strings(self):
        """
        Smoke tests on str() and unicode()
        """

        for cls in [IndependentMoney, Beneficiary, CommitteeBenefactor,
                    CorporationBenefactor, PersonBenefactor, Benefactor,
                    Form, Committee]:
            if cls.objects.all().count() == 0:  # bad :(
                continue
            obj = cls.objects.all()[0]
            self.assertNotIn('Object', str(obj), cls.__name__)
            self.assertNotIn('Object', unicode(obj), cls.__name__)

            self.assertNotEqual('', str(obj), cls.__name__)
            self.assertNotEqual('', unicode(obj), cls.__name__)
