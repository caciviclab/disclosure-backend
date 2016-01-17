"""
Command to download and load California campaign finance data from Netfile.
"""

import datetime
import warnings
from dateutil.parser import parse as date_parse
from numbers import Number

import numpy as np
import pandas as pd
from django.db import transaction

from ... import models
from ballot.models import Ballot
from locality.models import City, State, ZipCode
from netfile_raw.management.commands import downloadnetfilerawdata
from office_election.models import Office, OfficeElection, Candidate
from referendum.models import Referendum, ReferendumSelection


def isnan(val):
    return isinstance(val, Number) and np.isnan(val)


def isnone(val):
    return val is None or val == 'None'


def parse_benefactor(row, verbosity=1):
    # Benefactor info
    bf_state, _ = State.objects.get_or_create(
        short_name=row.get('tran_ST', 'Unknown'))
    bf_city, _ = City.objects.get_or_create(
        short_name=row.get('tran_City', 'Unknown'), state=bf_state)
    bf_zip_code, _ = ZipCode.objects.get_or_create(
        short_name=str(row.get('tran_Zip4', 'Unknown')), state=bf_state)

    if row['entity_Cd'] == 'IND':  # individual
        benefactor = models.PersonBenefactor(
            first_name=row.get('tran_NamF', None),
            last_name=row['tran_NamL'],
            occupation=row.get('tran_Occ'))
        benefactor.save()

    elif row['entity_Cd'] == 'OTH':  # corporation
        benefactor, _ = models.CorporationBenefactor.objects \
            .get_or_create(name=row['tran_NamL'])

    elif row['entity_Cd'] in ['SCC', 'COM']:  # committee
        # Get by name
        benefactor = get_committee_benefactor(row)
        filer_id = clean_filer_id(row.get('cmte_Id', ''))
        if filer_id is not None and benefactor.filer_id != filer_id:
            if benefactor.filer_id is None:
                if verbosity:
                    print("\n\nFIXED ID for %s\n\n" % benefactor.name)
                benefactor.filer_id = filer_id
            else:
                raise Exception("Conflicting committee ID for %s: "
                                "%s (saved) vs. %s (current)" % (
                                    benefactor.name,
                                    benefactor.filer_id,
                                    filer_id))

        # of=official, pf=primarily, ic=independent
        benefactor.name = row['tran_NamL'].strip()
        benefactor.type = benefactor.type or 'PF'  # TODO: fix
        benefactor.city = bf_city
        benefactor.state = bf_state
        benefactor.zip_code = bf_zip_code
        benefactor.locality = bf_city
        benefactor.save()

    elif row['entity_Cd'] == 'PTY':  # political party
        raise NotImplementedError("Form 460 Sched. A contributions "
                                  "from political parties.")

    else:
        raise ValueError("Entity type not expected: %s" % (
            row['entity_Cd']))

    return benefactor, bf_zip_code


def parse_form_and_report_period(row, verbosity=1):
    # Create/get the relevant form objects.
    f460A, _ = models.Form.objects.get_or_create(  # noqa
        name='460 Schedule A', text_id='460A',
        submission_frequency='SA')

    report_date = date_parse(row['tran_Date'])
    reporting_period, _ = models.ReportingPeriod.objects.get_or_create(
        form=f460A,
        period_start=datetime.datetime(report_date.year, 1, 1),
        period_end=datetime.datetime(report_date.year, 12, 31))

    return reporting_period


def parse_beneficiary(row, agency, verbosity=1):
    # Parse and save the beneficiary, contribution.
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

    beneficiary = get_committee_beneficiary(row)
    beneficiary.locality = locality
    beneficiary.name = row['filerName'].strip()
    beneficiary.type = 'PF'  # ok
    # beneficiary.address = '?'  # TODO: fix
    beneficiary.save()
    return beneficiary


def parse_candidate_and_office(row, verbosity=1):
    import re
    res = (
        # David Alvarez for Mayor 2014
        '^(?P<name>.*?)\s+for\s+(?P<office>.*?)(?P<year>[0-9]+).*$',
        # Scott Sanborn City Council 2016
        '^(?P<name>.*? .*?)\s+(?P<office>.*?)(?P<year>[0-9]+).*$',
    )

    # Either find a match, or raise an error.
    for re_str in res:
        matches = re.match(re_str, row['filerName'])
        if matches is not None:
            matches = matches.groupdict()
            break
    if matches is None:
        raise ValueError("Could not parse a Candidate.")

    name_parts = matches['name'].strip().split(" ")
    last_name = name_parts[-1]
    first_name = " ".join(name_parts[:-1]).strip() or None
    office = matches['office'].strip()
    return last_name, first_name, office


def parse_candidate_info(row, ballot, verbosity=1):
    # Try to get candidate name from beneficiary name.
    last_name, first_name, office_name = parse_candidate_and_office(
        row, verbosity=verbosity)
    candidate_office, _ = Office.objects.get_or_create(
        name=office_name, locality=ballot.locality)
    office_election, _ = OfficeElection.objects.get_or_create(
        office=candidate_office, ballot=ballot)
    candidate, _ = Candidate.objects.get_or_create(
        first_name=first_name, last_name=last_name,
        office_election=office_election)
    return candidate


def parse_referendum_info(row, ballot, verbosity=1):
    referendum, _ = Referendum.objects.get_or_create(
        name='Unknown', ballot=ballot)
    selection, _ = ReferendumSelection.objects.get_or_create(
        ballot_item=referendum,
        in_favor=True)
    return selection


def parse_ballot_info(row, locality, verbosity=1):
    ballot = Ballot.from_date(date=date_parse(row['tran_Date']),
                              locality=locality)

    # Figure out beneficiary from past entries.
    past_money = models.IndependentMoney.objects.filter(
        beneficiary__name=row['filerName'],
        beneficiary__ballot_item_selection__ballot_item__ballot=ballot)
    if past_money.count() > 0:
        # Figure it out from past contributions.
        ballot_item_selection = past_money[0] \
            .beneficiary.ballot_item_selection
    else:
        # Figure out beneficiary from item text.
        try:
            ballot_item_selection = parse_candidate_info(
                row, ballot=ballot, verbosity=verbosity)
        except ValueError:
            ballot_item_selection = parse_referendum_info(
                row, ballot=ballot, verbosity=verbosity)

    return ballot_item_selection, True


def get_committee_benefactor(row):
    """ Utility function to identify a committee benefactor.
    """
    return models.CommitteeBenefactor.objects.get_or_create(
        name=row['tran_NamL'].strip(),
        filer_id=clean_filer_id(row.get('cmte_Id', '')))[0]


def get_committee_beneficiary(row):
    """ Utility function to identify a committee beneficiary.
    """
    filer_id = row['filerId']
    if '-' in filer_id:
        filer_id = '-'.join(filer_id.split('-')[1:])
    else:
        filer_id = filer_id

    return models.Beneficiary.objects.get_or_create(
        name=row['filerName'].strip(), filer_id=filer_id)[0]


def clean_filer_id(filer_id):
    """ Utility function to scrub committee IDs."""
    if isinstance(filer_id, Number):
        return str(int(filer_id))
    elif np.any([filer_id.startswith(c) for c in ('C', '#')]):
        filer_id = filer_id[1:]
    return filer_id or None  # don't do blank.


@transaction.atomic
def load_f460A_row(row, agency, verbosity=1):  # noqa
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
    benefactor, bf_zip_code = parse_benefactor(
        row, verbosity=verbosity)
    reporting_period = parse_form_and_report_period(
        row, verbosity=verbosity)
    beneficiary = parse_beneficiary(
        row, agency=agency, verbosity=verbosity)
    beneficiary.ballot_item_selection, beneficiary.support = parse_ballot_info(
        row, locality=beneficiary.locality, verbosity=verbosity)
    beneficiary.save()

    # Now we have all the parts, save!
    money = models.IndependentMoney(  # or calculated_Amount
        amount=float(row['tran_Amt1']),
        report_date=date_parse(row['tran_Date']),
        reporting_period=reporting_period,
        benefactor_zip=bf_zip_code,
        benefactor=benefactor,
        beneficiary=beneficiary,
        source='NF',
        source_xact_id=row['netFileKey'])
    money.save()

    if verbosity:
        print(str(money))


def load_f460A_data(data, agency_fn, verbosity=1):  # noqa
    """ Loads data from Form 460 Schedule A:
    contributions to primarily formed committees."""

    print("Loading %d rows of Form 460 Sched. A data." % len(data))

    # Parse out the contributor information.
    error_rows = []
    for ri, (_, raw_row) in enumerate(data.T.iteritems()):
        assert raw_row['rec_Type'] == 'RCPT'
        minimal_row = raw_row.copy()

        # remove useless columns for easier exploring
        for col in minimal_row.keys():
            if isnone(minimal_row[col]) or isnan(minimal_row[col]):
                del minimal_row[col]

        # Store errors, for review later.
        try:
            agency = agency_fn(minimal_row)
            load_f460A_row(minimal_row, agency=agency, verbosity=verbosity)
        except Exception as ex:
            raise
            error_rows.append((ri, raw_row, minimal_row, ex))

    return error_rows


class Command(downloadnetfilerawdata.Command):
    help = 'Download and load the netfile raw data into the clean database.'

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
            self.header("There are %d rows in %s" % (
                        len(self.data), self.combined_csv_path))

        # Check for any potentially missing data.
        form_types = self.data['form_Type'].unique()
        if len({None, np.nan} - set(form_types)) != 2:
            warnings.warn("Some data don't have form_Type set.")

        f460A_data = self.data[self.data['form_Type'] == 'A']
        error_rows = load_f460A_data(data=f460A_data, verbosity=self.verbosity,
                                     agency_fn=lambda row: self.get_agency(
                                         row['filerId'].split('-')[0]))

        # Report errors  TODO: push to the database.
        if len(error_rows) > 0:
            print("Encountered %d errors; debug!" % len(error_rows))
            print("Errors:\n%s" % ','.join([e[-1] for e in error_rows]))

        # f497_data = self.data[self.data['form_Type'] == 'F497P2']
        # load_f497_data(data=f497_data, verbosity=verbosity)

        # f496_data = self.data[self.data['form_Type'] == 'F496P3']
        # load_f496_data(data=f496_data, verbosity=verbosity)

    def get_agency(self, agency_shortcut):
        agency_matches = filter(lambda a: a['shortcut'] == agency_shortcut,
                                self.agencies_metadata)
        if len(agency_matches) == 0:
            return None
        else:
            return agency_matches[0]
