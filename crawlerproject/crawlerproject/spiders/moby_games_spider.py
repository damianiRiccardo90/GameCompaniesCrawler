# crawlerproject/spiders/moby_games_spider.py

"""
This spider fetches all the game studios main pages available on 
https://www.mobygames.com/

Feeds the resulting urls to a csv file for eventual further processing.
"""

from scrapy import Request, Spider

class MobyGamesSpider(Spider):
    name = 'moby_games_spider'
    base_url = 'https://www.mobygames.com/'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'FEEDS': {
            'moby_companies.csv': {
                'format': 'csv',
                'fields': ['website'],
                'encoding': 'utf8',
            },
        }
    }

    start_urls = ['https://www.mobygames.com/company/page:0/']

    # Set the total number of pages
    total_pages = 200

    def parse(self, response):
        # Follow the company pages
        company_links = response.css('a[href^="/company"]::attr(href)').getall()
        for link in company_links:
            full_link = response.urljoin(link)
            self.logger.info(f'Following company on: {full_link}')
            yield Request(url=full_link, callback=self.parse_company)

        # Get the current page number from the URL
        current_page = int(response.url.split('page:')[1].rstrip('/'))

        # Check if there are more pages to scrape, if so make a request for next page
        if current_page < self.total_pages - 1:
            next_page = current_page + 1
            next_page_url = self.base_url + f'company/page:{next_page}/'
            self.logger.info(f'Crawling to next page: {next_page_url}')
            yield Request(next_page_url, callback=self.parse)

    def parse_company(self, response):
        # Extract the first link under "Related Web Sites"
        company_page = response.css('section#companySites ul.list-group li a::attr(href)').get()
        if company_page:
            self.logger.info(f'Found company page: {company_page}')
            yield {'website': company_page}
