import scrapy
from itemloaders.processors import Join, MapCompose

import re


# removing escape chachters  such as (\n\t,...)
def remove_escapes(s):
    return re.sub("[^A-Za-z0-9-']+", ' ', s).strip()


# get only numeric value
def pricing(s):
    return re.sub("[^0-9]", '', s)


# alternating title
def titling(s):
    return re.sub("[^0-9]", '', s) + ' bedroom flat for rental'


class Property(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_escapes, titling), output_processor=Join())
    price = scrapy.Field(input_processor=MapCompose(pricing), output_processor=Join())
    url = scrapy.Field(output_processor=Join())
