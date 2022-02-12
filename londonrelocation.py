import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.extractor)
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

