"""
Command to download and load California campaign finance data from Netfile.
"""

import os
import csv
import cStringIO
import codecs

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

class UnicodeDictWriter(object):
    """
    A CSV DictWriter which will write rows to CSV file "f",
    which is encoded in the given encoding.

    Adapted from https://docs.python.org/2/library/csv.html#examples
    """

    def __init__(self, f, headers, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, headers, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writeheader(self):
        self.writer.writeheader()

    def writerow(self, row):
        utf8_row = dict()
        for k, v in row.iteritems():
            utf8_row[k] = codecs.encode(unicode(v), 'utf-8')

        self.writer.writerow(utf8_row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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

        try:
            item = iterator.next()
        except StopIteration:
            self.failure('No data')
            return

        with open(os.path.join(DATA_DIR, csv_path), 'w') as csv_handle:
            headers = item.keys()
            writer = UnicodeDictWriter(csv_handle, headers)
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
