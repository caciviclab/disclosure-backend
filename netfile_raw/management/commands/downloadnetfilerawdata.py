"""
Command to download and load California campaign finance data from Netfile.
"""

import os
import os.path as op
import csv
import cStringIO
import codecs
import warnings

import calaccess_raw
from calaccess_raw.management.commands import loadcalaccessrawfile
from django.conf import settings
from optparse import make_option

from netfile_raw.connect2_api import Connect2API


custom_options = (
    make_option(
        "--agencies",
        action="store",
        dest="agencies",
        default=None,
        help="Agency names to query (comma-separated)"
    ),
    make_option(
        "--years",
        action="store",
        dest="years",
        default=None,
        help="Years to query (comma-separated)"
    ),
    make_option(
        "--max-lines",
        action="store",
        dest="max_lines_per_load",
        default=1000,
        type=int,
        help="Max # lines to load, per query"
    ),
    make_option(
        "--force",
        action="store_true",
        dest="force",
        default=False,
        help="Re-download files that already exist?"
    ),
    make_option(
        "--skip-download",
        action="store_true",
        dest="skip_download",
        default=False,
        help="Skip downloading of the raw data"
    ),
    make_option(
        "--skip-combine",
        action="store_true",
        dest="skip_combine",
        default=False,
        help="Skip combining of the downloaded data"
    ),
    make_option(
        "--skip-load",
        action="store_true",
        dest="skip_load",
        default=False,
        help="Skip loading up the raw data files"
    ),
)


def get_download_directory():
    """
    Returns the download directory where we will store downloaded data.
    """
    if hasattr(settings, 'NETFILE_DOWNLOAD_DIR'):
        return getattr(settings, 'NETFILE_DOWNLOAD_DIR')
    else:
        return calaccess_raw.get_download_directory()


def get_test_download_directory():
    """
    Returns the download directory where we will store test data.
    """
    if hasattr(settings, 'CALACCESS_TEST_DOWNLOAD_DIR'):
        return getattr(settings, 'CALACCESS_TEST_DOWNLOAD_DIR')
    elif hasattr(settings, 'BASE_DIR'):
        return os.path.join(getattr(settings, 'BASE_DIR'), 'test-data')
    raise ValueError("CAL-ACCESS test download directory not configured. \
Set either CALACCESS_TEST_DOWNLOAD_DIR or BASE_DIR in settings.py")


class UnicodeDictWriter(object):
    """
    A CSV DictWriter which will write rows to CSV file "f",
    which is encoded in the given encoding.

    Adapted from https://docs.python.org/2/library/csv.html#examples
    """
    def __init__(self, f, headers, dialect=csv.excel, encoding="utf-8",
                 **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, headers, dialect=dialect, **kwds)
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


class Command(loadcalaccessrawfile.Command):
    help = 'Download and load the Netfile raw data'
    app_name = 'netfile_raw'
    option_list = loadcalaccessrawfile.Command.option_list + custom_options
    # netfile gives us ISO8601 formatted dates, so we have to override the
    # calaccess_raw date hack with a slightly different one :)
    date_sql = "DATE_FORMAT(str_to_date(@`%s`, '%%Y-%%m-%%d'), '%%Y-%%m-%%d')"

    def handle(self, *args, **options):
        # Parse command-line options
        self.csv = None
        self.database = options['database']
        self.verbosity = int(options['verbosity'])
        self.max_lines_per_load = int(options['max_lines_per_load'])
        if options['agencies'] is None:
            self.agencies = []
        else:
            self.agencies = options['agencies'].split(',')
        if options['years'] is None:
            self.years = []
        else:
            self.years = options['years'].split(',')
        self.force = options['force']

        # Compute properties
        self.data_dir = os.path.join(get_download_directory(), 'csv')
        self.agency_csv_path = op.join(self.data_dir, 'netfile_agency.csv')
        self.combined_csv_path = os.path.join(
            self.data_dir, 'netfile_cal201_transaction.csv')

        # Run the thing!
        if not options['skip_download']:
            self.download()

        if not options['skip_combine']:
            self.combine()

        if not options['skip_load']:
            self.load()

    def download(self):
        if self.verbosity:
            self.header("Downloading raw data files")

        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)

        # Fetch agencies
        agencies = self.fetch_agencies()
        agency_keys = [ag['shortcut'] for ag in agencies]
        agencies_not_found = set(self.agencies) - set(agency_keys)

        if len(self.agencies) == 0:
            self.agencies = agency_keys
        elif len(agencies_not_found) > 0:
            warnings.warn('Could not find these agencies: %s' % (
                ','.join(agencies_not_found)))
            self.agencies = list(set(self.agencies) - agencies_not_found)
        agencies = filter(lambda ag: ag['shortcut'] in self.agencies,
                          agencies)  # filter agencies by shortcut

        # Scrub years
        years = ['2014', '2015']
        years_not_found = set(self.years) - set(years)
        if len(self.years) == 0:
            self.years = years
        elif len(years_not_found) > 0:
            warnings.warn('Could not find these years: %s' % (
                ','.join(years_not_found)))
            self.years = list(set(self.years) - years_not_found)

        if self.verbosity:
            print("Downloading data for %d agencies in years %s" % (
                len(agencies), ','.join(self.years)))
        self.csv_paths = []
        for agency in agencies:
            for year in self.years:
                csv_path = 'netfile_%s_%s_cal201_export.csv' % (
                    year, str(agency['shortcut']))
                csv_path = os.path.join(self.data_dir, csv_path)
                # Only download on demand.
                if self.force or not op.exists(csv_path):
                    transactions = self.fetch_transactions_agency_year(
                        agency, year)
                    self._write_csv(csv_path, transactions)
                self.csv_paths.append(csv_path)

    def combine(self):
        if self.verbosity:
            self.header("Combining %s csv files." % len(self.csv_paths))

        headers_written = False
        with file(self.combined_csv_path, 'w') as combined_csv:
            for path in self.csv_paths:
                agency_shortcut = os.path.basename(path).split('_')[2]
                with file(path, 'r') as agency_csv:
                    header_line = agency_csv.readline()
                    if header_line == '':
                        continue
                    headers = ','.join(
                        ['agency_shortcut', header_line])
                    if not headers_written:
                        combined_csv.write(headers)
                        headers_written = headers
                    else:
                        # make sure things don't go all wierd between files.
                        assert headers == headers_written
                    for line in agency_csv.readlines():
                        combined_csv.write(','.join([agency_shortcut, line]))

    def load(self):
        if self.verbosity:
            self.header("Loading Agency CSV file")
        super(Command, self).load(
            'NetFileAgency', csv_path=self.agency_csv_path)
        if self.verbosity:
            self.success("ok.")
        if self.verbosity:
            self.header("Loading Cal201 Transaction Data")
        super(Command, self).load(
            'NetFileCal201Transaction', csv_path=self.combined_csv_path)
        if self.verbosity:
            self.success("ok.")

    def _write_csv(self, csv_path, iterator):
        if not csv_path.startswith(self.data_dir):
            csv_path = os.path.join(self.data_dir, csv_path)

        if self.verbosity:
            self.log('Writing %s...' % op.abspath(csv_path))

        try:
            item = iterator.next()
        except StopIteration:
            self.failure('No data')
            with open(csv_path, 'w') as csv_handle:
                pass  # create empty csv, to enable caching.
        else:
            with open(csv_path, 'w') as csv_handle:
                headers = item.keys()
                writer = UnicodeDictWriter(
                    csv_handle, headers, lineterminator='\n')
                writer.writeheader()
                writer.writerow(item)
                for item in iterator:
                    writer.writerow(item)

            if self.verbosity:
                self.success('OK')

    @property
    def connect2(self):
        """ Connecting to netfile is slow, so only do it on demand."""
        if getattr(self, '_connect2', None) is None:
            self._connect2 = Connect2API()
        return self._connect2

    def fetch_transactions_agency_year(self, agency, year):
        # Break this up by transaction type?
        query = {
            'Aid': agency['id'],
            'Year': year,
            'sortOrder': 1,  # DateDescending
        }

        return self.connect2.postpubliccampaignexportcal201transactionyear(
            query)

    def fetch_agencies(self):
        """Fetches agencies from Netfile API"""
        agencies = None
        if not self.force and op.exists(self.agency_csv_path):
            import pandas as pd
            try:
                agencies = pd.read_csv(self.agency_csv_path)
                agencies = agencies.T.to_dict().values()
            except:
                os.remove(self.agency_csv_path)

        if agencies is None:
            agencies = self.connect2.getpubliccampaignagencies()
            self._write_csv(self.agency_csv_path, iter(agencies))

        if self.verbosity:
            print("Found %s agencies" % (len(agencies)))
        return agencies
