import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    # extracting all areas
    def parse(self, response):
        areas = response.xpath('//*[@class="gallery-slide-wrap row-flex wrap-flex round-button"]')
        areas_links = areas[0].xpath('.//h4/a/@href').extract()
        for area in areas_links:
            yield scrapy.Request(area, callback=self.extractor)

    # extract data from area
    def extractor(self, response):
        for card in response.xpath('//*[@class="test-inline"]'):
            l = ItemLoader(item=Property(), selector=card)
            url = card.xpath('.//*[@class="h4-space"]/h4/a/@href').extract_first()

            l.add_value('title', response.xpath('//*[@class="bottom-ic"]/p/text()').extract_first())
            l.add_value('price', card.xpath('.//*[@class="bottom-ic"]/h5/text()').extract_first())
            l.add_value('url', response.urljoin(url))
            yield l.load_item()

        # checking if we reched to the 2nd page
        if '&pageset=2' not in response.url:
            nextPage = response.url + '&pageset=2'
            yield scrapy.Request(nextPage, callback=self.extractor)

