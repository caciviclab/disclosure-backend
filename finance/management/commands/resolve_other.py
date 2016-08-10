from django.core.management.base import BaseCommand

from ...models import Employer, OtherBenefactor


class Command(BaseCommand):
    help = 'Set up the test server'
    # option_list = custom_options

    def handle(self, *args, **options):
        for committee in OtherBenefactor.objects.all():
            employers = Employer.objects.filter(name__iexact=committee.name)
            if employers.count() == 0:
                continue

            print(committee, employers[0])
