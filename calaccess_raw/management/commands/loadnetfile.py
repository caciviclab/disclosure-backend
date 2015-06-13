from __future__ import unicode_literals
from optparse import make_option
from calaccess_raw.management.commands import CalAccessCommand


custom_options = (
    make_option(
        "--skip-download",
        action="store_false",
        dest="download",
        default=True,
        help="Skip downloading of the ZIP archive"
    ),
)


class Command(CalAccessCommand):
    help = 'Download NetFile data'
    option_list = CalAccessCommand.option_list + custom_options

    def set_options(self, *args, **kwargs):
        self.query_url = 'https://netfile.com:443/Connect2/api/public/campaign/search/transaction/query'
        self.verbosity = int(kwargs['verbosity'])

    def handle(self, *args, **options):
        pass


