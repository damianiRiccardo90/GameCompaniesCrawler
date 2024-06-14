# crawlerproject/spiders/main_page_spider.py

"""
This spider goes through all the game studios main pages available on wikipedia
for game studios and indie studios as well.

It creates a file where all of them are listed for further processing.
"""

from scrapy import Request, Spider

class MainPageSpider(Spider):
    name = 'main_page_spider'

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
        },
        'FEEDS': {
            'companies.csv': {
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
            self.logger.debug(f"Starting request for URL: {url}")
            yield Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Select all rows with the specified background color indicating alive companies
        for row in response.css('tr[style*="background:#c9daff;"]'):
            # Extract the link in the first cell of the row
            link = row.css('td:first-child a::attr(href)').get()
            if link:
                full_url = response.urljoin(link)
                yield Request(full_url, callback=self.parse_company)     
        
    def parse_company(self, response):
        self.logger.debug(f"Parsing company URL: {response.url}")
        # Extract the website URL
        website = response.css('td.infobox-data span.url a::attr(href)').get()
        yield {
            'website': website,
        }
