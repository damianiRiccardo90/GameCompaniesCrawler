# crawlerproject/spiders/gamedevmap_spider.py

"""
This spider fetches all the game studios main pages available on 
https://www.gamedevmap.com/

Feeds the resulting urls to a csv file for eventual further processing.
"""

from scrapy import Request, Spider

class GameDevMapSpider(Spider):
    name = 'gamedevmap_spider'
    base_url = 'https://www.gamedevmap.com/'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'FEEDS': {
            'gamedevmap_companies.csv': {
                'format': 'csv',
                'fields': ['website'],
                'encoding': 'utf8',
            },
        }
    }
    
    start_urls = ['https://www.gamedevmap.com/']

    def parse(self, response):
        # Extract countries from the dropdown
        countries = response.css('select#countryDropdown option::attr(value)').getall()
        
        # Remove the first option since it is "All countries"
        countries = countries[1:]

        # Now you can use these countries to generate requests dynamically
        for country in countries:
            country_url = self.base_url + f'index.php?country={country}&state=&city=&query=&type='
            self.logger.info(f'Crawling to: {country_url}')
            yield Request(url=country_url, callback=self.parse_country)

    def parse_country(self, response):
        # Extract the company websites from the table
        rows = response.css('tr.row1, tr.row2')
        for row in rows:
            website = row.css('td a::attr(href)').get()
            if website:
                self.logger.debug(f'Found company page: {website}')
                yield {
                    'website': website
                }

    def parse(self, response):
        pass

    def parse_company(self, response):
        pass
