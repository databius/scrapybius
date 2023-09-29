# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatabiusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SvgItem(scrapy.Item):
    name = scrapy.Field()
    ref = scrapy.Field()
    file_urls = scrapy.Field()
