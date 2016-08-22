from __future__ import absolute_import
import factory
from factory.django import DjangoModelFactory

from ballot.tests.factory import CityFactory


class ZipCodeFactory(DjangoModelFactory):
    class Meta:
        model = 'locality.ZipCode'


class BenefactorFactory(DjangoModelFactory):
    class Meta:
        model = 'finance.Benefactor'

    benefactor_type = 'IF'
    benefactor_locality = factory.SubFactory(CityFactory)


class BeneficiaryFactory(DjangoModelFactory):
    class Meta:
        model = 'finance.Beneficiary'


class IndependentMoneyFactory(DjangoModelFactory):
    class Meta:
        model = 'finance.IndependentMoney'

    amount = 55.5
    beneficiary = factory.SubFactory(BeneficiaryFactory)
    benefactor = factory.SubFactory(BenefactorFactory)
    benefactor_zip = factory.SubFactory(ZipCodeFactory)
    report_date = factory.Faker('date_time')
    source = 'NF'
    source_xact_id = '1234'
