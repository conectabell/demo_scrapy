# from scrapy.selector import HtmlXPathSelector
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
import scrapy
from scrapy.utils.project import get_project_settings

"""
Lista las imágenes del html de un sitio web.
"""

DOMAIN = 'example.com'
# URL = 'http://%s' % DOMAIN

class IMGSpider(scrapy.Spider):
    name = DOMAIN
    settings = get_project_settings()
    allowed_domains = [DOMAIN]
    start_urls = settings.get('START_URLS')
    IMAGES_RESULT = []

    def imgstore(self, image):
        if image not in self.IMAGES_RESULT:
            self.IMAGES_RESULT.append(image)

    # Parse URLS y imagenes
    def parse(self, response):
        hxs = scrapy.selector.HtmlXPathSelector(response)
        # hxs.select('//dl[@class="clearfix"]//img/@src').extract()
        # hxs.select('//a/@href').extract():
        for url in hxs.select('//a/@href').extract():
            if not (url.startswith('http://') or url.startswith('https://')):
                url = self.start_urls[0] + "/" + url
            for image in hxs.select('//img/@src').extract():
                url_image = self.start_urls[0] + "/" + image
                self.imgstore(url_image)
            yield scrapy.http.Request(url, callback=self.parse)

    # Método para el cierre del spider
    def closed(self, reason):
        print("### IMAGENES Extraidas")
        print(self.IMAGES_RESULT)
