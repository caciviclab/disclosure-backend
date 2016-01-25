import logging

from swaggerpy.client import SwaggerClient

logger = logging.getLogger(__name__)

CONNECT2_SPEC = "https://netfile.com/Connect2/api/resources"


def paginated_query(func):
    """
    Paginated Query Decorator

    Decorates the query by returning a generator, making
    additional requests for each page of responses.
    """

    def _paginated_query(self, query):
        page_index = 0
        query.update({'currentPageIndex': page_index})

        while True:
            # Fetch the current page
            query['currentPageIndex'] = page_index
            response = func(self, query)
            assert response.status_code == 200

            # Report what was done.
            pages = response.json()['totalMatchingPages']
            logger.info("Fetched page %d of %d pages available" %
                        (page_index + 1, pages))

            # Return the results
            results = response.json()['results']
            for result in results:
                yield result

            # Increment the page count
            if page_index >= pages:
                break
            page_index += 1

    return _paginated_query


class Connect2API(object):
    """Netfile Connect2 API"""

    def __init__(self):
        self.api = SwaggerClient(CONNECT2_SPEC)

    def getpubliccampaignagencies(self):
        """
        GET /public/campaign/agencies
        """
        response = self.api.public.Agencies()
        assert response.status_code == 200

        data = response.json()
        assert 'agencies' in data

        return data['agencies']

    @paginated_query
    def postpubliccampaignexportcal201transactionyear(self, query):
        """
        POST /public/campaign/export/cal201/transaction/year
        """
        return self.api.public.ByYear(Year=query)
