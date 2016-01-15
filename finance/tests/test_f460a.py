import numpy as np

from django.test import TestCase

from finance.management.commands import xformnetfilerawdata as cmd


class FinanceParseTests(TestCase):

    def test_isnan(self):
        self.assertTrue(cmd.isnan(np.nan), "Test np.nan")

        self.assertFalse(cmd.isnan(1), "Test int")
        self.assertFalse(cmd.isnan(1.), "Test float")
        self.assertFalse(cmd.isnan(""), "Test empty string")
        self.assertFalse(cmd.isnan("str"), "Test string")

    def test_isnone(self):
        self.assertTrue(cmd.isnone(None), "Test None")
        self.assertTrue(cmd.isnone('None'), "Test 'None'")

        self.assertFalse(cmd.isnone('Non'), "Test 'Non'")
        self.assertFalse(cmd.isnone(0), "Test zero")
        self.assertFalse(cmd.isnone(''), "Test empty string")

    def test_parse_benefactor(self):
        # must use the different entity_Cd
        # def parse_benefactor(row, verbosity=1):
        pass

    def test_parse_form_and_report_period(self):
        pass

    def test_parse_beneficiary(self):
        pass

    def test_parse_candidate_and_office(self):
        pass

    def test_parse_candidate_info(self):
        pass

    def test_parse_referendum_info(self):
        pass

    def test_parse_ballot_info(self):
        pass

    def test_get_committee_benefactor(self):
        pass

    def test_get_committee_beneficiary(self):
        pass

    def test_clean_filer_id(self):
        pass

    def test_load_f460A_row(self):  # noqa
        pass

    def test_load_f460A_data(self):  # noqa
        pass
