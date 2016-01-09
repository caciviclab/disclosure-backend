"""
Command to download and load California campaign finance data from Netfile.
"""

import os.path as op
import time
import warnings
from dateutil.parser import parse as date_parse
from numbers import Number

import numpy as np
import pandas as pd

from ... import models
from ballot_measure.models import Ballot, BallotMeasure
from candidate.models import Person, Office, Election, Candidate
from locality.models import Address, City, State, ZipCode
from netfile_raw.management.commands import downloadnetfilerawdata


class Command(downloadnetfilerawdata.Command):
    help = 'Download and load the netfile raw data into the clean database.'

    def join_data_descr(self, df):
        """ Used to print column descriptions; helpful for devs.

        You can get this csv file from:
        https://data.sfgov.org/City-Management-and-Ethics/Campaign-Finance-Data-Key/wygs-cc76
        """
        descr_csv = op.join(self.data_dir, 'Campaign_Finance_-_Data_Key.csv')
        if not op.exists(descr_csv):
            return df

        all_descr = pd.read_csv(descr_csv)
        cols = all_descr['Column'].str.lower().tolist()

        our_descr = dict()
        for key in df:
            our_descr[key] = None
            lkey = key.lower()
            if lkey not in cols:
                # print("%s: no description found." % key)
                continue
            our_descr[key] = all_descr['Description'].iloc[cols.index(lkey)]

        # Print the results
        for key in sorted(our_descr.keys()):
            vals = [str(v) for v in sorted(df[key].unique())]
            if len(vals) > 1:
                print('%-15s: %s, %s' % (
                    key, (str(our_descr[key]) or '')[:30],
                    (','.join(vals))[:30]))
            # else:
            #     print('Skipping: %s' % key)
        return df

    def load(self):
        """
        According to:
        https://github.com/caciviclab/caciviclab.github.io/wiki/Campaign-Finance

        To get a comprehensive total of the amount of money raised for
        any ballot measure, you must include:
        * Form 460, Schedules A (monetary contributions) and
            C (nonmonetary contributions), for all Primarily Formed and
            Candidate Controlled committees
        * Form 497, beginning from the ending period of the last Form 460 that
            was filed, for all Primarily Formed and
            Candidate Controlled committees
        * Form 496, only expenses in support, only from committees that
            are NOT the Primarily Formed or Candidate Controlled committees,
            and only those beginning from the ending period of the
            last Form 460 that was filed
        """
        if self.verbosity:
            self.header("Loading disclosure data into database.")

        self.data = pd.read_csv(self.combined_csv_path)
        if self.verbosity:
            print("There are %d rows in %s" % (
                len(self.data), self.combined_csv_path))

        # Check for any potentially missing data.
        form_types = self.data['form_Type'].unique()
        if len({None, np.nan} - set(form_types)) != 2:
            warnings.warn("Some data don't have form_Type set.")

        self.load_f460A_data()
        if self.verbosity:
            print(form_types)
        self.load_f497_data()
        self.load_f496_data()

    def load_f460A_data(self):  # noqa
        """ Loads data from Form 460 Schedule A:
        contributions to primarily formed committees."""

        # Split data by type, add column defs.
        self.f460A_data = self.data[self.data['form_Type'] == 'A']
        self.f460A_data = self.join_data_descr(self.f460A_data)

        def isnan(val):
            return isinstance(val, Number) and np.isnan(val)

        def isnone(val):
            return val is None or val == 'None'

        # Parse out the contributor information.
        error_rows = []
        for ri, (_, raw_row) in enumerate(self.f460A_data.T.iteritems()):
            assert raw_row['rec_Type'] == 'RCPT'
            minimal_row = raw_row.copy()

            # remove useless columns for easier exploring
            for col in minimal_row.keys():
                if isnone(minimal_row[col]) or isnan(minimal_row[col]):
                    del minimal_row[col]

            # Store errors, for review later.
            try:
                self.load_f460A_row(minimal_row)
            except Exception as e:
                raise
                if self.verbosity:
                    print("%d: \n\n%s\n\n" % (len(error_rows) + 1, e))
                    time.sleep(0.5)
                error_rows.append((ri, raw_row, minimal_row, e))

        # Report errors.
        if len(error_rows) > 0:
            if self.verbosity:
                print("Encountered %d errors; debug!" % len(error_rows))
            import pdb
            pdb.set_trace()

    def get_agency(self, agency_shortcut):
        agency_matches = filter(lambda a: a['shortcut'] == agency_shortcut,
                                self.agencies_metadata)
        if len(agency_matches) == 0:
            return None
        else:
            return agency_matches[0]

    def load_f460A_row(self, row):  # noqa
        """ Loads an individual row from Form 460 Schedule A. # noqa
        This is where most of the magic happens!

        Some metadata:
        ^ calculated_Amount: None, -294.84,-200.0,50.0,99.0,100.0
        x calculated_Date: None, 2015-01-07T00:00:00.0000000-08
        ^ cmte_Id        : Committee ID # (If [COM|RCP] &, nan,#890268,1244975,1264568,12
        ^ entity_Cd      : Contributor Type of Entity (In, COM,IND,OTH,SCC
        ^ filerId        : None, COA-113952,COA-113968,COA-1139
        ^ filerName      : None, Better Transportation for Alam
        x filingId       : None, 155104080,155521798,155524068,
        x intr_City      : Intermediary City, nan,Alameda
        x intr_NamL      : Intermediary Last Name, nan,Wilma Chan For Supervisor
        x intr_ST        : Intermediary State, nan,CA
        x intr_Zip4      : Intermediary Zip, nan,94501
        x netFileKey     : None, 00bab3072253498da017a4e60105ea
        ^ tran_Amt1      : Transaction Amount, -200.0,-294.84,100.0,1000.0,10
        ^ tran_Amt2      : Cumulative Year-To-Date, -6867.12,0.0,100.0,1000.0,101.
        tran_City      : Transaction Entity's City, Alameda,Alamo,Arcata,Atherton,
        tran_Date      : Transaction Date, 2015-01-07T00:00:00.0000000-08
        tran_Date1     : Transaction Date (if a range), 2013-10-03T00:00:00.0000000-07
        tran_Emp       : Transaction Entity's Employer, nan,ABCO Wire & Metal Products
        tran_Id        : Transaction ID # (not necessar, 1DOCUB61ZGyZ,21mtbGMusZdR,22Lp
        tran_NamF      : Transaction Entity's First Nam, nan,Albert,Alice,Andrew,Andy,A
        tran_NamL      : Transaction Entity's Last Name, ABC Security  Service Inc,ACME
        tran_Occ       : Transaction Entity's Occupatio, nan,Actuary,Acupuncturist,Acup
        tran_ST        : None, CA,MO,TX
        tran_Type      : Transaction Type (T=Third Part, nan,R,X
        tran_Zip4      : Transaction Entity's Zip Code, 63105,75702,75711,90036,90040,
        """

        def parse_benefactor(row):
            # Benefactor info
            bf_state, _ = State.objects.get_or_create(
                short_name=row.get('tran_ST', 'Unknown'))
            bf_city, _ = City.objects.get_or_create(
                short_name=row.get('tran_City', 'Unknown'), state=bf_state)
            bf_zip_code, _ = ZipCode.objects.get_or_create(
                short_name=row.get('tran_Zip4', 'Unknown'), state=bf_state)
            bf_address, _ = Address.objects.get_or_create(
                city=bf_city, state=bf_state, zip_code=bf_zip_code)

            if row['entity_Cd'] == 'IND':  # individual
                benefactor = models.IndividualBenefactor(
                    first_name=row.get('tran_NamF', ''),
                    last_name=row['tran_NamL'],
                    occupation=row.get('tran_Occ'))
                benefactor.save()

            elif row['entity_Cd'] == 'OTH':  # company
                benefactor, _ = models.CompanyBenefactor.objects.get_or_create(
                    name=row['tran_NamL'])

            elif row['entity_Cd'] in ['SCC', 'COM']:  # committee
                # Get by name
                benefactor = self.get_committee_benefactor(row)
                cmte_id = self.clean_cmte_id(row.get('cmte_Id', ''))
                if cmte_id != '' and benefactor.committee_id != cmte_id:
                    if benefactor.faked:
                        if self.verbosity:
                            print("\n\nFIXED ID for %s\n\n" % benefactor.name)
                        benefactor.committee_id = cmte_id
                        benefactor.faked = False
                    else:
                        raise Exception("Conflicting committee ID for %s: "
                                        "%s (saved) vs. %s (current)" % (
                                            benefactor.name,
                                            benefactor.committee_id,
                                            cmte_id))

                # of=official, pf=primarily, ic=independent
                benefactor.name = row['tran_NamL'].strip()
                benefactor.type = benefactor.type or 'PF'  # TODO: fix
                benefactor.address = bf_address
                benefactor.locality = bf_city
                benefactor.save()

            elif row['entity_Cd'] == 'PTY':  # political party
                raise NotImplementedError("Form 460 Sched. A contributions "
                                          "from political parties.")

            else:
                raise ValueError("Entity type not expected: %s" % (
                    row['entity_Cd']))

            return benefactor, bf_zip_code
        benefactor, bf_zip_code = parse_benefactor(row)

        def parse_form_and_report_period(row):
            # Create/get the relevant form objects.
            f460A, _ = models.Form.objects.get_or_create(  # noqa
                name='460 Schedule A', text_id='460A',
                submission_frequency='SA')

            reporting_period, _ = models.ReportingPeriod.objects.get_or_create(
                period_start=date_parse(row['tran_Date']),
                period_end=date_parse(row['tran_Date']))

            return f460A, reporting_period
        f460A, reporting_period = parse_form_and_report_period(row)  # noqa

        def parse_beneficiary(row):
            # Parse and save the beneficiary, contribution.
            agency_shortcut = row['filerId'].split('-')[0]
            agency = self.get_agency(agency_shortcut)
            if agency:
                state, _ = State.objects.get_or_create(short_name='CA')
                if state.name is None or state.name == '':
                    state.name = 'California'
                    state.save()
                locality, _ = City.objects.get_or_create(
                    short_name=agency['shortcut'], name=agency['name'],
                    state=state)
            else:
                locality = None

            beneficiary = self.get_committee_beneficiary(row)
            beneficiary.locality = locality
            beneficiary.name = row['filerName'].strip()
            beneficiary.type = 'PF'  # ok
            # beneficiary.address = '?'  # TODO: fix
            beneficiary.save()
            return beneficiary
        beneficiary = parse_beneficiary(row)

        def parse_ballot_info(row, locality):
            ballot, _ = Ballot.objects.get_or_create(
                date=date_parse(row['tran_Date']), locality=locality)
            ballot_measure, _ = BallotMeasure.objects.get_or_create(
                contest_type='O', name='?', number='?', ballot=ballot)

            candidate_person, _ = Person.objects.get_or_create(
                first_name='?', last_name='?')
            candidate_office, _ = Office.objects.get_or_create(
                name='?', description='?', locality=locality)
            candidate_election, _ = Election.objects.get_or_create(
                office=candidate_office, ballot_measure=ballot_measure)

            candidate, _ = Candidate.objects.get_or_create(
                person=candidate_person, election=candidate_election,
                ballot_measure=ballot_measure
                # title = models.CharField(max_length=255)
                # subtitle = models.CharField(max_length=255, blank=True)
                # brief = models.TextField(blank=True)
                # full_text = models.TextField(blank=True)
                # pro_statement = models.TextField(blank=True)
                # con_statement = models.TextField(blank=True)
            )
            return candidate
        candidate = parse_ballot_info(row, locality=beneficiary.locality)

        # Now we have all the parts, save!
        money = models.IndependentMoney(  # or calculated_Amount
            amount=row['tran_Amt1'], support=True,  # TODO
            benefactor_zip=bf_zip_code,
            form=f460A, reporting_period=reporting_period,
            benefactor=benefactor, beneficiary=beneficiary,
            ballot_measure_choice=candidate,
            filing_id=row['filingId'],
            source='NF', source_xact_id=row['netFileKey'])
        money.save()

        if self.verbosity:
            print(str(money)[:75])

    def get_committee(self, model, name, id=None):
        """ Utility function to identify a committee benefactor.

        This is hard because sometimes the committee ID is missing!
        """

        if id:
            # Use committee ID first.
            benefactor, _ = model.objects.get_or_create(
                committee_id=self.clean_cmte_id(id))
        else:
            # Try by name second.
            try:
                benefactor = model.objects.get(name=name)
            except model.DoesNotExist:
                # Make a new committee based on name only, third
                benefactor = model(name=name)
                benefactor.committee_id = name
                benefactor.faked = True
                if self.verbosity:
                    print('\n\nFaked benefactor %s :(\n\n' % benefactor.name)

        return benefactor

    def get_committee_benefactor(self, row):
        """ Utility function to identify a committee benefactor.
        """
        return self.get_committee(model=models.CommitteeBenefactor,
                                  name=row['tran_NamL'].strip(),
                                  id=row.get('cmte_Id'))

    def get_committee_beneficiary(self, row):
        """ Utility function to identify a committee beneficiary.
        """
        filer_id = row['filerId']
        if '-' in filer_id:
            committee_id = '-'.join(filer_id.split('-')[1:])
        else:
            committee_id = filer_id

        return self.get_committee(model=models.Beneficiary,
                                  name=row['filerName'].strip(),
                                  id=committee_id)

    @staticmethod
    def clean_cmte_id(cmte_id):
        """ Utility function to scrub committee IDs."""
        if isinstance(cmte_id, Number):
            return str(int(cmte_id))
        elif np.any([cmte_id.startswith(c) for c in ('C', '#')]):
            cmte_id = cmte_id[1:]
        return cmte_id

    def load_f497_data(self):
        """ Loads data from Form 460 Schedule A:
        contributions to primarily formed committees."""
        # Split data by type, add column defs.
        self.f497_data = self.data[self.data['form_Type'] == 'F497P2']
        if self.verbosity:
            print("NYI: load %d rows of form 497 data." % len(self.f497_data))

    def load_f496_data(self):
        # Split data by type, add column defs.
        self.f496_data = self.data[self.data['form_Type'] == 'F496P3']
        if self.verbosity:
            print("NYI: load %d rows of form 496 data." % len(self.f496_data))
