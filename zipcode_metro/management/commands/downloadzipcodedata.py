"""
Command to download and load ZipCode/Metro/PSA data
"""

import os
import csv
import requests
import zipfile

from calaccess_raw.management.commands import loadcalaccessrawfile
from django.db import connection
from optparse import make_option


DATA_DIR = 'zipcode_raw_data'

custom_options = (
    make_option(
        "--skip-download",
        action="store_false",
        dest="skip_download",
        default=False,
        help="Skip downloading of the raw data"
    ),
    make_option(
        "--skip-load",
        action="store_false",
        dest="skip_load",
        default=False,
        help="Skip loading up the raw data files"
    ),
)

class Command(loadcalaccessrawfile.Command):
    help = 'Download and load the Zipcode raw data'
    url = "https://s3-us-west-1.amazonaws.com/zipcodemetro/zipcode_metro.csv.zip"
    option_list = loadcalaccessrawfile.Command.option_list + custom_options

    def handle(self, *args, **options):
        self.verbosity = int(options['verbosity'])
        self.max_lines_per_load = int(options.get('max_lines_per_load'))
        self.zip_path = os.path.join(DATA_DIR, 'zipcode_metro.zip')

        if not options['skip_download']:
            self.download()

        if not options['skip_load']:
            self.cursor = connection.cursor()
            self.load()


    def download(self):
        if self.verbosity:
            self.header("Downloading/unzipping raw data files")

        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)

        r = requests.get(self.url)
        with open(self.zip_path, 'wb') as f:
            f.write(r.content)
            f.close()

        with zipfile.ZipFile(self.zip_path) as zf:
            zf.extract('zipcode_metro.csv', DATA_DIR)

        if self.verbosity:
            self.success('ok.')

    def load(self):
        if self.verbosity:
            self.header("Loading CSV files")
        super(Command, self).load('zipcode_metro.ZipCodeMetro')
        if self.verbosity:
            self.success('ok.')
