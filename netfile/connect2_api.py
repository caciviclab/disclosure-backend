import json
import csv
import sys

from swaggerpy.client import SwaggerClient

CONNECT2_SPEC = "https://netfile.com/Connect2/api/resources"

class Connect2API(object):
    """Netfile Connect2 API"""

    def __init__(self):
        self.api = SwaggerClient(CONNECT2_SPEC)

    def getpubliccampaignagencies(self):
        """
        GET /pubic/campaign/agencies
        """
        response = self.api.public.getpubliccampaignagencies()
        assert response.status_code == 200

        data = response.json()
        assert data.has_key('agencies')

        return data['agencies']

    def postpubliccampaignsearchtransactionquery(self, query):
        """
        POST /public/campaign/search/transaction/query
        """
        page_index = 0
        query.update({
            'currentPageIndex': page_index,
            })

        response = self.api.public.postpubliccampaignsearchtransactionquery(Query=query)
        assert response.status_code == 200

        pages = response.json()['totalMatchingPages']
        print "%d pages available" % (pages)
        pages = max(pages, 2) #TODO Once the queries are set, unlimit this. For now, limit to two pages of data

        results = response.json()['results']
        while True:
            page_index += 1
            for result in results:
                yield result

            if page_index >= pages:
                break

            # Fetch another page
            query['currentPageIndex'] = page_index
            response = self.api.public.postpubliccampaignsearchtransactionquery(Query=query)
            assert response.status_code == 200
            results = response.json()['results']


def demo():
    connect2 = Connect2API()
    csvfile = sys.stdout

    # Agencies
    agencies = connect2.getpubliccampaignagencies()
    headers = agencies[0].keys()
    agency_csv = csv.DictWriter(csvfile, headers)
    agency_csv.writeheader()
    for agency in agencies:
        agency_csv.writerow(agency)

    transactions = connect2.postpubliccampaignsearchtransactionquery({
        'Agency': 52, # SF Ethics Commission
        #'Agency': 129, # California SOS
        #'transactionType': 30, # Form 460
        'DateStart': '2015-01-01T00:00:00Z',
        'sortOrder': 1, # DateDescending
        })

    # Transactions in SF
    transaction = transactions.next() # Work-around generator magic
    headers = transaction.keys()
    transaction_csv = csv.DictWriter(csvfile, headers)
    transaction_csv.writeheader()
    for transaction in transactions:
        transaction_csv.writerow(transaction)


if __name__ == '__main__':
    demo()
