"""
Command to download and load California campaign finance data from Netfile.
"""

import os
import csv

from calaccess_raw.management.commands import CalAccessCommand
from optparse import make_option

from netfile.connect2_api import Connect2API

DATA_DIR = 'netfile_raw_data'

custom_options = (
    make_option(
        "--skip-download",
        action="store_false",
        dest="download",
        default=True,
        help="Skip downloading of the raw data"
    ),
    make_option(
        "--skip-load",
        action="store_false",
        dest="load",
        default=True,
        help="Skip loading up the raw data files"
    ),
)

class Command(CalAccessCommand):
    help = 'Download and load the Netfile raw data'
    option_list = CalAccessCommand.option_list + custom_options

    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])
        self.connect2 = Connect2API()

        if options['download']:
            self.download()

        if options['load']:
            self.load()

    def download(self):
        if self.verbosity:
            self.header("Downloading raw data files")

        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)

        # Fetch agencies
        agencies = self.fetch_agencies()
        print "Found %s agencies" %  (len(agencies))
        self._write_csv('agencies.csv', iter(agencies))

        for agency in agencies:

            for year in ['2014']:
                csv_path = '%s_%s_cal201_export.csv' % (year, agency['shortcut'])
                transactions = self.fetch_transactions_agency_year(agency, year)
                self._write_csv(csv_path, transactions)

    def load(self):
        pass

    def _write_csv(self, csv_path, iterator):
        if self.verbosity:
            self.log('Writing %s...' % (csv_path))

        with open(os.path.join(DATA_DIR, csv_path), 'w') as csv_handle:
            try:
                item = iterator.next()
            except StopIteration:
                self.failure('No data')
                return

            headers = item.keys()
            writer = csv.DictWriter(csv_handle, headers)
            writer.writeheader()
            writer.writerow(item)
            for item in iterator:
                writer.writerow(item)

        if self.verbosity:
            self.success('OK')

    def fetch_transactions_agency_year(self, agency, year):
        # Break this up by transaction type?
        query = {
            'Aid': agency['id'],
            'Year': year,
            'sortOrder': 1, # DateDescending
            }

        return self.connect2.postpubliccampaignexportcal201transactionyear(query)


    def fetch_agencies(self):
        """Fetches agencies from Netfile API"""
        return self.connect2.getpubliccampaignagencies()

