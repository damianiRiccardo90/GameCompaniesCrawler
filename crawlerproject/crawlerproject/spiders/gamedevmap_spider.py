# crawlerproject/spiders/gamedevmap_spider.py

"""
This spider fetches all the game studios main pages available on 
https://www.gamedevmap.com/

Feeds the resulting urls to a csv file for eventual further processing.
"""
""" REPLACED BY FILE BASED SOLUTION DUE TO ENCODING ISSUES
from scrapy import Request, Spider
from scrapy.http import TextResponse

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
        # Convert the response to a TextResponse
        response = TextResponse(url=response.url, body=response.body, encoding='utf-8')

        # Extract countries from the dropdown
        countries = response.css('select#countryDropdown option::attr(value)').getall()
        
        # Remove the first option since it is "All countries"
        countries = countries[1:]
        self.logger.info(f'Dio merdoso: {countries}')

        # Now you can use these countries to generate requests dynamically
        for country in countries:
            country_url = self.base_url + f'index.php?country={country}&state=&city=&query=&type='
            self.logger.info(f'Crawling to: {country_url}')
            yield Request(url=country_url, callback=self.parse_country)

    def parse_country(self, response):
        # Convert the response to a TextResponse
        response = TextResponse(url=response.url, body=response.body, encoding='utf-8')

        # Extract the company websites from the table
        rows = response.css('tr.row1, tr.row2')
        for row in rows:
            website = row.css('td a::attr(href)').get()
            if website:
                self.logger.debug(f'Found company page: {website}')
                yield {
                    'website': website
                }
"""
from scrapy import Spider, Request
from scrapy.http import TextResponse
import pkg_resources
import os

class GameDevMapSpider(Spider):
    name = 'gamedevmap_spider'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 0,  # No delay between requests
        'CONCURRENT_REQUESTS': 100,  # Increase the number of concurrent requests
        'RETRY_ENABLED': False,  # Disable retry middleware
        'REDIRECT_ENABLED': False,  # Disable redirect middleware
        'COOKIES_ENABLED': False,  # Disable cookies middleware
        'TELNETCONSOLE_ENABLED': False,  # Disable telnet console
        'AUTOTHROTTLE_ENABLED': False,  # Disable AutoThrottle
        'DOWNLOADER_MIDDLEWARES': {},  # Disable all downloader middlewares
        'SPIDER_MIDDLEWARES': {},  # Disable all spider middlewares
        'FEEDS': {
            'gamedevmap_companies.csv': {
                'format': 'csv',
                'fields': ['website'],
                'encoding': 'utf8',
            },
        }
    }

    def start_requests(self):
        files = [
            'data/gamedevmap/algeria.html',
            'data/gamedevmap/argentina.html',
            'data/gamedevmap/armenia.html',
            'data/gamedevmap/australia1.html',
            'data/gamedevmap/australia2.html',
            'data/gamedevmap/austria.html',
            'data/gamedevmap/azerbaijan.html',
            'data/gamedevmap/bahrain.html',
            'data/gamedevmap/bangladesh.html',
            'data/gamedevmap/belarus.html',
            'data/gamedevmap/belgium.html',
            'data/gamedevmap/bosnia_and_herzegovina.html',
            'data/gamedevmap/brasil.html',
            'data/gamedevmap/brazil1.html',
            'data/gamedevmap/brazil2.html',
            'data/gamedevmap/brunei.html',
            'data/gamedevmap/bulgaria.html',
            'data/gamedevmap/cameroon.html',
            'data/gamedevmap/canada1.html',
            'data/gamedevmap/canada2.html',
            'data/gamedevmap/canada3.html',
            'data/gamedevmap/canada4.html',
            'data/gamedevmap/canada5.html',
            'data/gamedevmap/canada6.html',
            'data/gamedevmap/canada7.html',
            'data/gamedevmap/cayman_islands.html',
            'data/gamedevmap/chile.html',
            'data/gamedevmap/china1.html',
            'data/gamedevmap/china2.html',
            'data/gamedevmap/colombia.html',
            'data/gamedevmap/costa_rica.html',
            'data/gamedevmap/croatia.html',
            'data/gamedevmap/cyprus.html',
            'data/gamedevmap/czech_republic.html',
            'data/gamedevmap/denmark.html',
            'data/gamedevmap/ecuador.html',
            'data/gamedevmap/egypt.html',
            'data/gamedevmap/el_salvador.html',
            'data/gamedevmap/england1.html',
            'data/gamedevmap/england2.html',
            'data/gamedevmap/england3.html',
            'data/gamedevmap/england4.html',
            'data/gamedevmap/england5.html',
            'data/gamedevmap/england6.html',
            'data/gamedevmap/england7.html',
            'data/gamedevmap/estonia.html',
            'data/gamedevmap/ethiopia.html',
            'data/gamedevmap/finland1.html',
            'data/gamedevmap/finland2.html',
            'data/gamedevmap/france1.html',
            'data/gamedevmap/france2.html',
            'data/gamedevmap/france3.html',
            'data/gamedevmap/france4.html',
            'data/gamedevmap/georgia.html',
            'data/gamedevmap/germany1.html',
            'data/gamedevmap/germany2.html',
            'data/gamedevmap/germany3.html',
            'data/gamedevmap/germany4.html',
            'data/gamedevmap/ghana.html',
            'data/gamedevmap/greece.html',
            'data/gamedevmap/guatemala.html',
            'data/gamedevmap/hungary.html',
            'data/gamedevmap/iceland.html',
            'data/gamedevmap/india1.html',
            'data/gamedevmap/india2.html',
            'data/gamedevmap/indonesia.html',
            'data/gamedevmap/iran.html',
            'data/gamedevmap/iraq.html',
            'data/gamedevmap/ireland.html',
            'data/gamedevmap/israel.html',
            'data/gamedevmap/italy1.html',
            'data/gamedevmap/italy2.html',
            'data/gamedevmap/jamaica.html',
            'data/gamedevmap/japan1.html',
            'data/gamedevmap/japan2.html',
            'data/gamedevmap/japan3.html',
            'data/gamedevmap/jordan.html',
            'data/gamedevmap/kazakhstan.html',
            'data/gamedevmap/kenya.html',
            'data/gamedevmap/kuwait.html',
            'data/gamedevmap/latvia.html',
            'data/gamedevmap/lebanon.html',
            'data/gamedevmap/libya.html',
            'data/gamedevmap/liechtenstein.html',
            'data/gamedevmap/lithuania.html',
            'data/gamedevmap/luxembourg.html',
            'data/gamedevmap/macedonia.html',
            'data/gamedevmap/malaysia.html',
            'data/gamedevmap/malta.html',
            'data/gamedevmap/mexico.html',
            'data/gamedevmap/moldova.html',
            'data/gamedevmap/morocco.html',
            'data/gamedevmap/myanmar.html',
            'data/gamedevmap/netherlands1.html',
            'data/gamedevmap/netherlands2.html',
            'data/gamedevmap/new_zealand.html',
            'data/gamedevmap/nigeria.html',
            'data/gamedevmap/northern_ireland.html',
            'data/gamedevmap/norway.html',
            'data/gamedevmap/pakistan.html',
            'data/gamedevmap/palestine.html',
            'data/gamedevmap/paraguay.html',
            'data/gamedevmap/peru.html',
            'data/gamedevmap/philippines.html',
            'data/gamedevmap/poland1.html',
            'data/gamedevmap/poland2.html',
            'data/gamedevmap/portugal.html',
            'data/gamedevmap/qatar.html',
            'data/gamedevmap/remote.html',
            'data/gamedevmap/romania.html',
            'data/gamedevmap/russia1.html',
            'data/gamedevmap/russia2.html',
            'data/gamedevmap/saudi_arabia.html',
            'data/gamedevmap/scotland.html',
            'data/gamedevmap/senegal.html',
            'data/gamedevmap/serbia.html',
            'data/gamedevmap/singapore.html',
            'data/gamedevmap/slovakia.html',
            'data/gamedevmap/slovenia.html',
            'data/gamedevmap/south_africa.html',
            'data/gamedevmap/south_korea1.html',
            'data/gamedevmap/south_korea2.html',
            'data/gamedevmap/spain1.html',
            'data/gamedevmap/spain2.html',
            'data/gamedevmap/sri_lanka.html',
            'data/gamedevmap/sweden1.html',
            'data/gamedevmap/sweden2.html',
            'data/gamedevmap/sweden3.html',
            'data/gamedevmap/switzerland.html',
            'data/gamedevmap/syria.html',
            'data/gamedevmap/taiwan.html',
            'data/gamedevmap/thailand.html',
            'data/gamedevmap/tunisia.html',
            'data/gamedevmap/turkey.html',
            'data/gamedevmap/ukraine.html',
            'data/gamedevmap/united_arab_emirates.html',
            'data/gamedevmap/united_states1.html',
            'data/gamedevmap/united_states2.html',
            'data/gamedevmap/united_states3.html',
            'data/gamedevmap/united_states4.html',
            'data/gamedevmap/united_states5.html',
            'data/gamedevmap/united_states6.html',
            'data/gamedevmap/united_states7.html',
            'data/gamedevmap/united_states8.html',
            'data/gamedevmap/united_states9.html',
            'data/gamedevmap/united_states10.html',
            'data/gamedevmap/united_states11.html',
            'data/gamedevmap/united_states12.html',
            'data/gamedevmap/united_states13.html',
            'data/gamedevmap/united_states14.html',
            'data/gamedevmap/united_states15.html',
            'data/gamedevmap/united_states16.html',
            'data/gamedevmap/united_states17.html',
            'data/gamedevmap/united_states18.html',
            'data/gamedevmap/united_states19.html',
            'data/gamedevmap/united_states20.html',
            'data/gamedevmap/united_states21.html',
            'data/gamedevmap/united_states22.html',
            'data/gamedevmap/united_states23.html',
            'data/gamedevmap/uruguay.html',
            'data/gamedevmap/venezuela.html',
            'data/gamedevmap/vietnam.html',
            'data/gamedevmap/wales.html',
            'data/gamedevmap/zimbabwe.html',
        ]
        """
        for file in files:
            file_path = pkg_resources.resource_filename('crawlerproject', file)
            self.logger.info(f'Reading file: {file_path}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                response = TextResponse(url=file_path, body=content, encoding='utf-8')

                rows = response.css('tr.row1, tr.row2')
                for row in rows:
                    website = row.css('td a::attr(href)').get()
                    if website:
                        self.logger.debug(f'Found company page: {website}')
                        yield {'website': website}
        """
        for file in files:
            file_path = pkg_resources.resource_filename('crawlerproject', file)
            file_url = f'file:///{os.path.abspath(file_path)}'
            self.logger.info(f'Reading file: {file_path}')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                response = TextResponse(url=file_url, body=content, encoding='utf-8')
                yield Request(url=file_url, callback=self.parse, meta={'response': response})

    def parse(self, response):
        response = response.meta['response']

        # Correcting the selector to match your HTML structure
        rows = response.css('tr.row1, tr.row2')
        for row in rows:
            website = row.css('td a::attr(href)').get()
            if website:
                self.logger.debug(f'Found company page: {website}')
                yield {'website': website}
            else:
                self.logger.error(f'No website found in row: {row.extract()}')
