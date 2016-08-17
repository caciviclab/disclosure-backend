import os.path as op

from django.test import TestCase

import numpy as np
import pandas as pd

from ballot.models import Party
from finance.management.commands.xformnetfilerawdata import (
    clean_city, clean_name, clean_state, clean_zip, isnan, isnone,
    parse_benefactor)


class XformNetfileRawDataUnitTest(TestCase):
    """Unit tests on generic methods within the command file."""
    def test_isnan(self):
        """Test isnan function."""
        self.assertTrue(isnan(np.nan))
        self.assertFalse(isnan('nan'))
        self.assertFalse(isnan(''))

    def test_isnone(self):
        """Test isnone function."""
        self.assertTrue(isnone(None))
        self.assertTrue(isnone('None'))
        self.assertFalse(isnone(''))

    def test_clean_name(self):
        """Test clean_name function."""
        self.assertEqual(clean_name(None), None)
        self.assertEqual(clean_name(''), '')
        self.assertEqual(clean_name('my city'), 'My City')
        self.assertEqual(clean_name('my city, ca'), 'My City, Ca')

    def test_clean_city(self):
        """Test clean_city function."""
        self.assertEqual(clean_city(None), None)
        self.assertEqual(clean_city(''), '')
        self.assertEqual(clean_city('my city'), 'My City')
        self.assertEqual(clean_city('my city, ca'), 'My City')

    def test_clean_state(self):
        """Test clean_state function."""
        self.assertEqual(clean_state(None), None)
        self.assertEqual(clean_state(''), '')
        self.assertEqual(clean_state('my state'), 'MY STATE')

    def test_clean_zip(self):
        """Test clean_zip function."""
        self.assertEqual(clean_zip(None), None)
        self.assertEqual(clean_zip(''), '')
        self.assertEqual(clean_zip('Abc'), 'ABC')
        self.assertEqual(clean_zip('Abc 123'), 'ABC 123')
        self.assertEqual(clean_zip('12345'), '12345')
        self.assertEqual(clean_zip('12345-6789'), '12345')
        self.assertEqual(clean_zip(12345), '12345')


class XformNetfileRawDataPTYTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(XformNetfileRawDataPTYTest, cls).setUpClass()

        # A count of Party objects is used in test assertion
        Party.objects.all().delete()

        cls.PTY_CSV_FILE = op.join(
            op.dirname(__file__), 'data', 'test_PTY.csv')

    def test_PTY(self):
        self.data = pd.read_csv(self.PTY_CSV_FILE)
        row = self.data.iloc[0]
        benefactor, _ = parse_benefactor(row)
        self.assertEqual(benefactor.benefactor_type, 'PY')
        self.assertEqual(Party.objects.all().count(), 1)
