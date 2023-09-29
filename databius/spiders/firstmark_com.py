import json

import scrapy

from databius.items import SvgItem
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
                "Accept-Encoding": "gzip, deflate",
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
            img_url = company.get("Processed Logo URL")
            if img_url.endswith(".svg"):
                yield SvgItem(name=name, category=category, sub_category=sub_category, file_urls=[img_url])

        pass
