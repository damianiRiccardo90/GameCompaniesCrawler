# crawlerproject/spiders/main_page_spider.py

"""
This spider goes through all the game studios main pages available on
https://gamecompanies.com/industries/

It creates a file where all of them are listed for further processing.
"""

import scrapy
from scrapy_selenium import SeleniumRequest

class MainPageSpider(scrapy.Spider):
    name = "main_page_spider"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy_selenium.SeleniumMiddleware': 800,
        },
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': 'path/to/chromedriver',
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless'],  # '--headless' if using chrome instead of firefox
    }

    # Add your target URLs here
    start_urls = [
        'https://gamecompanies.com/industries/north-american-game-industry/companies',
        'https://gamecompanies.com/industries/south-american-game-industry/companies',
        'https://gamecompanies.com/industries/european-game-industry/companies',
        'https://gamecompanies.com/industries/nordic-game-industry/companies',
        'https://gamecompanies.com/industries/baltic-game-industry/companies',
        'https://gamecompanies.com/industries/asian-game-industry/companies',
        'https://gamecompanies.com/industries/african-game-industry/companies',
        'https://gamecompanies.com/industries/oceania-game-industry/companies'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"Access denied to {response.url}")
            return

        self.logger.debug(f"Parsing {response.url}")

        # Extract all company links within divs
        company_links = response.css('div.ItemListItem-root a::attr(href)').getall()
        for link in company_links:
            yield response.follow(link, self.parse_company)
    
    def parse_company(self, response):
        pass
