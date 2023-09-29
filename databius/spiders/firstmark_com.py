import json
import logging
import time
from urllib.parse import urlparse

import scrapy

from databius.items import LogoItem
from databius.settings import DEFAULT_REQUEST_HEADERS

DOWNLOAD_DIR = "./data"


class FirstmarkSpider(scrapy.Spider):
    name = "firstmark.com"
    base_url = "https://mad.firstmark.com/"

    custom_settings = {
        "ITEM_PIPELINES": {
            "databius.pipelines.SvgPipeline": 1,
        },
        "FILES_STORE": DOWNLOAD_DIR
    }

    def start_requests(self):
        yield scrapy.Request(
            f"{self.base_url}_next/data/oI3bcdx35s1gwbW5Ce6HJ/index.json",
            headers={
                **DEFAULT_REQUEST_HEADERS,
                "Host": "mad.firstmark.com",
            },
            method="GET"
        )

    def parse(self, response):
        raw = json.loads(response.body)
        for company in raw["pageProps"]["companies"]:
            """
              {
                "Company Name": "Institute for Ethical AI & Machine Learning",
                "Category": "Machine Learning & Artificial Intelligence",
                "Sub Category": "Horizontal AI/AGI",
                "URL": "https://ethical.institute/",
                "Description": "\n",
                "Linked Category": [
                  "recrAqXmw72gb32V5"
                ],
                "Linked SubCategory": [
                  "recpg9ydFPHPhB4Jc"
                ],
                "Processed Logo URL": "https://res.cloudinary.com/dl0nekgpw/image/upload/MAD%202023/Institute_for_Ethical_AI_vxdlcm.png",
                "Sort Index": 29
              }
            """
            name = company.get("Company Name")
            category = company.get("Category")
            sub_category = company.get("Sub Category")
            url = company.get("URL")
            img_url = company.get("Processed Logo URL")

            meta = {"name": name, "category": category, "sub_category": sub_category, "url": url}

            logging.info(f"Got: {category}||{sub_category}||{name}||{url}")
            yield LogoItem(name=name, category=category, sub_category=sub_category, file_urls=[img_url])

            if not img_url.endswith(".svg"):
                yield self.wikimedia_requests(meta)
                time.sleep(1)

    def wikimedia_requests(self, meta):
        domain = urlparse(meta['url']).netloc
        search = domain + "+" + meta['name'].replace(" ", "+") + "+logo"
        search_url = f'https://commons.wikimedia.org/w/index.php?search="{search}"&filemime=svg&title=Special:MediaSearch&go=Go&type=image'
        logging.info(f"[{meta['name']}] Searching by {search_url}")
        return scrapy.Request(
            search_url,
            headers={
                **DEFAULT_REQUEST_HEADERS,
                "Host": "commons.wikimedia.org",
            },
            method="GET",
            meta={**meta, "ref": search_url},
            callback=self.parse_wikimedia
        )

    def parse_wikimedia(self, response):
        search_results = response.xpath('//div[@class="sdms-search-results"]//a')
        for search_result in search_results:
            href = search_result.xpath('@href').get()
            logging.info(f"[{response.meta['name']}] Got wikimedia file: {href}")
            if href.endswith(".svg"):
                return self.wikimedia_svg_requests(href, response.meta)

    def wikimedia_svg_requests(self, url, meta):
        logging.info(f"[{meta['name']}] Request wikimedia files: {url}")
        return scrapy.Request(
            url,
            headers={
                **DEFAULT_REQUEST_HEADERS,
                "Host": "commons.wikimedia.org",
            },
            method="GET",
            meta=meta,
            callback=self.parse_wikimedia_file
        )

    def parse_wikimedia_file(self, response):
        files = response.xpath('//div[@class="fullMedia"]//a')
        for file in files:
            file_url = file.xpath('@href').get()
            logging.info(f"[{response.meta['name']}] Got Logo: {file_url}")
            return LogoItem(
                name=f'{response.meta["name"]}',
                category=response.meta["category"],
                sub_category=response.meta["sub_category"],
                ref=response.meta["ref"],
                file_urls=[file_url]
            )
