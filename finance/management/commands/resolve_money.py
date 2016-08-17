from django.core.management.base import BaseCommand

from ...models import IndependentMoney


class Command(BaseCommand):
    help = 'Set up the test server'
    # option_list = custom_options

    def handle(self, *args, **options):

        for im in IndependentMoney.objects.all().order_by('-amount'):
            related_money = IndependentMoney.objects.filter(
                amount=im.amount,
                benefactor=im.benefactor, beneficiary=im.beneficiary)
            if related_money.count() <= 1:
                continue
            related_money = list(related_money)
            if related_money.index(im) > 0:
                continue

            print related_money.index(im), str(im)
            for rm in related_money:
                print "\t%s %10s %s %s %s" % (
                    rm.report_date, rm.filing_id,
                    rm.source_xact_id, rm.benefactor)
