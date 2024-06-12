# crawlerproject/spiders/main_page_spider.py

"""
This spider goes through all the game studios main pages available on
https://gamecompanies.com/industries/

It creates a file where all of them are listed for further processing.
"""

from scrapy_playwright.http import PlaywrightRequest
from scrapy import Spider

class MainPageSpider(Spider):
    name = 'main_page_spider'
    allowed_domains = ['mobygames.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
            'scrapy_playwright.middleware.PlaywrightMiddleware': 543,
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }

    # Add your target URLs here
    start_urls = [f'https://www.mobygames.com/company/page:{i}/' for i in range(205)]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        for url in self.start_urls:
            yield PlaywrightRequest(url, self.parse, wait_until='networkidle')

    def parse(self, response):
        # Log the response URL to verify the request was successful
        self.logger.debug(f'Parsing URL: {response.url}')
        
        # Extract company details from the table rows
        companies = response.css('div.overflow-x-scroll > table > tbody > tr')
        self.logger.debug(f'Found {len(companies)} companies')
        
        for company in companies:
            url = company.css('td a::attr(href)').get()
            
            # Follow the company link to scrape additional details
            if url:
                self.logger.debug(f'Following URL: {url}')
                yield response.follow(url, self.parse_company)
            else:
                self.logger.debug('No URL found for a company row')

    def parse_company(self, response):
        try:
            # Extract the first link under "Related Web Sites"
            first_related_site = response.css('section#companySites ul.list-group li a::attr(href)').get()

            if first_related_site:
                # Ensure the file exists before writing
                with open('output_urls.txt', 'a') as f:
                    f.write(first_related_site + '\n')
        except Exception as e:
            self.logger.error(f"Error parsing company: {e}")
