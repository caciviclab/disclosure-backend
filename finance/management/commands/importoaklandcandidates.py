import csv
import datetime
import urllib2

from django.core.management.base import BaseCommand

from ballot.models import Ballot, Candidate, Office, OfficeElection
from locality.models import City, State
from ballot.models.referendum import Referendum


HUMAN_CANDIDATES_URL = \
    'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=0&single=true&output=tsv'
BALLOT_MEASURES_URL = \
    'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=1693935349&single=true&output=tsv'
NON_CONTROLLED_COMMITTEE_URL = \
    'https://docs.google.com/spreadsheets/d/1272oaLyQhKwQa6RicA5tBso6wFruum-mgrNm3O3VogI/pub?gid=1995437960&single=true&output=tsv'

class Command(BaseCommand):
    help = 'Import the Oakland Candidates from the spreadsheet'

    def handle(self, *args, **options):
        # BALLOT:
        state, _ = State.objects.get_or_create(name='California', short_name='CA')
        oakland, _ = City.objects.get_or_create(
            name='Oakland',
            short_name='COAK',
            state=state
        )

        ballot, _ = Ballot.objects.get_or_create(
            locality=oakland
        )
        ballot.date = datetime.date(2016, 11, 6)
        ballot.save()

        # HUMAN CANDIDATES
        # =====================================================================
        self.process_humans(ballot, oakland)

        # BALLOT MEASURES
        # =====================================================================
        self.process_ballot_measures(ballot)

    def process_ballot_measures(self, ballot):
        resp = urllib2.urlopen(BALLOT_MEASURES_URL)
        rows = csv.DictReader(resp, delimiter='\t')
        title_column = 'Ballot Measures:  ' \
            'https://drive.google.com/open?id=0BzmHYSKNqcR_TjdjY21icWt6VUE'
        for row in rows:
            referendum, created = Referendum.objects.get_or_create(
                title=row[title_column],
                number=row['Measure alpha-numeric designation'],
                contest_type='R',
                ballot=ballot
            )
            if created:
                print 'created!'
            else:
                print referendum
        resp.close()

    def process_humans(self, ballot, oakland):
        resp = urllib2.urlopen(HUMAN_CANDIDATES_URL)
        rows = csv.DictReader(resp, delimiter='\t')
        for row in rows:
            # TODO: Update the spreadsheet to handle split names
            names = row['Candidate'].split(' ', 3)
            if len(names) == 2:
                first_name = names[0]
                middle_name = ''
                last_name = names[1]
            elif len(names) > 2:
                first_name = names[0]
                middle_name = " ".join(names[1:-1])
                last_name = " ".join(names[-1:])

            candidate_office, _ = Office.objects.get_or_create(
                name=row['Office'],
                locality=oakland
            )
            office_election, _ = OfficeElection.objects.get_or_create(
                office=candidate_office,
                ballot=ballot
            )

            candidate = Candidate.objects.filter(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                office_election=office_election
            )

            if candidate:
                print "Found existing candidate: " + str(candidate)
            else:
                candidate.get_or_create(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    office_election=office_election
                )
                print "Creating candidate: " + str(candidate)
        resp.close()
