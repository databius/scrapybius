import scrapy


class ApacheOrgSpider(scrapy.Spider):
    name = "apache.org"
    allowed_domains = ["www.apache.org"]
    start_urls = ["https://www.apache.org/logos"]

    def parse(self, response):
        pass
