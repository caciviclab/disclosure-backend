from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


custom_options = (
    make_option(
        "--username",
        action="store",
        dest="username",
        default='admin',
        help="Admin username"
    ),
    make_option(
        "--password",
        action="store",
        dest="password",
        default='admin',
        help="Admin password"
    ),
)


class Command(BaseCommand):
    help = 'Set up the test server'
    option_list = custom_options

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('migrate', database='calaccess_raw')

        if User.objects.filter(username=options['username']).count() == 0:
            print("Adding superuser '%s'" % options['username'])
            User.objects.create_superuser(
                username=options['username'], password=options['password'], email='')
