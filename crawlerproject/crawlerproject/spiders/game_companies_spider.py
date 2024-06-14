# crawlerproject/spiders/game_companies_spider.py

"""
This spider fetches all the game studios main pages available on 
https://gamecompanies.com/

Feeds the resulting urls to a csv file for eventual further processing.
"""

from scrapy import Request, Spider
from scrapy.http import TextResponse
import pkg_resources

class GameCompaniesSpider(Spider):
    name = 'game_companies_spider'
    base_url = 'https://gamecompanies.com'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'FEEDS': {
            'game_companies.csv': {
                'format': 'csv',
                'fields': ['website'],
                'encoding': 'utf8',
            },
        },
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
        }
    }

    def start_requests(self):
        files = [
            'data/game_companies/africa.html',
            'data/game_companies/asia.html',
            'data/game_companies/baltics.html',
            'data/game_companies/europe.html',
            'data/game_companies/nordics.html',
            'data/game_companies/north_america.html',
            'data/game_companies/oceania.html',
            'data/game_companies/south_america.html'
        ]

        for file in files:
            file_path = pkg_resources.resource_filename('crawlerproject', file)
            self.logger.info(f'Reading file: {file_path}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                response = TextResponse(url=file_path, body=content, encoding='utf-8')
                yield from self.parse(response)

    def parse(self, response):
        # Select all the company links with the generic path and specific style attribute
        company_links = response.css('a[href^="/industries/"][style="text-decoration:none"]::attr(href)').getall()
        
        for link in company_links:
            full_url = self.base_url + link
            self.logger.info(f'Crawling to: {full_url}')
            yield Request(url=full_url, callback=self.parse_company)

    def parse_company(self, response):
        # Extract and log the URL of the company page
        self.logger.info(f'Found company page: {response.url}')
        yield {'website': response.url}
