from django.db import models
from django.test import TestCase

from _django_utils.serializers import as_money, ExtendedModelSerializer


class AsMoneyTest(TestCase):

    def test_good(self):
        """
        Smoke tests on str() and unicode()
        """
        self.assertEqual(0, as_money(0))
        self.assertEqual(1.5, as_money(1.5))
        self.assertEqual(1.51, as_money(1.51))
        self.assertTrue(1.496 < as_money(1.496))

    def test_evil(self):
        self.assertIsNone(as_money(None))


class DummyModel(models.Model):
    f1 = models.CharField()
    f2 = models.IntegerField()


class ExtendedModelSerializerTest(TestCase):
    def test_exclude_field(self):
        class DummySerializer(ExtendedModelSerializer):
            class Meta:
                model = DummyModel
                exclude = ['f2']

        self.assertIn('f1', DummySerializer().get_fields())
        self.assertNotIn('f2', DummySerializer().get_fields())

    def test_rename_field(self):
        class DummySerializer(ExtendedModelSerializer):
            class Meta:
                model = DummyModel
                rename = dict(f2='foo')

        self.assertIn('foo', DummySerializer().get_fields())
        self.assertNotIn('f2', DummySerializer().get_fields())
