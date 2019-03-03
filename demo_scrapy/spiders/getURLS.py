# from scrapy.selector import HtmlXPathSelector
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
import scrapy
from scrapy.utils.project import get_project_settings

"""
Lista todas las URL de un sitio web.
"""

DOMAIN = 'example.com'
# URL = 'http://%s' % DOMAIN


class URLSpider(scrapy.Spider):
    name = DOMAIN
    settings = get_project_settings()
    allowed_domains = [DOMAIN]
    start_urls = settings.get('START_URLS')
    URLS_RESULT = []

    def urlstore(self, url):
        self.URLS_RESULT
        if url not in self.URLS_RESULT:
            self.URLS_RESULT.append(url)

    # Parse URLS y imagenes
    def parse(self, response):
        hxs = scrapy.selector.HtmlXPathSelector(response)
        # hxs.select('//dl[@class="clearfix"]//img/@src').extract()
        # hxs.select('//a/@href').extract():
        for url in hxs.select('//a/@href').extract():
            if not (url.startswith('http://') or url.startswith('https://')):
                url = self.start_urls[0] + "/" + url
            self.urlstore(url)
            yield scrapy.http.Request(url, callback=self.parse)

    # Método para el cierre del spider
    def closed(self, reason):
        print("### URLS Extraidas")
        print(self.URLS_RESULT)
