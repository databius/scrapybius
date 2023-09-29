# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatabiusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LogoItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    ref = scrapy.Field()
    file_urls = scrapy.Field()
