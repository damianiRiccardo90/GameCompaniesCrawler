# crawlerproject/spiders/wikipedia_spider.py

"""
This spider goes through all the game studios main pages available on wikipedia
for game studios and indie studios as well.

Feeds the resulting urls to a csv file for eventual further processing.
"""

from scrapy import Request, Spider

class WikipediaSpider(Spider):
    name = 'wikipedia_spider'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'FEEDS': {
            'wikipedia_companies.csv': {
                'format': 'csv',
                'fields': ['website'],
                'encoding': 'utf8',
            },
        },
    }

    # Add your target URLs here
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_video_game_developers',
        'https://en.wikipedia.org/wiki/List_of_indie_game_developers'
    ]

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info(f"Starting request for URL: {url}")
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # Select all rows with the specified background color indicating alive companies
        for row in response.css('tr[style*="background:#c9daff;"]'):
            # Extract the link in the first cell of the row
            link = row.css('td:first-child a::attr(href)').get()
            if link:
                full_url = response.urljoin(link)
                yield Request(full_url, callback=self.parse_company)     
        
    def parse_company(self, response):
        self.logger.info(f"Parsing company URL: {response.url}")
        # Extract the website URL
        website = response.css('td.infobox-data span.url a::attr(href)').get()
        yield {
            'website': website,
        }
