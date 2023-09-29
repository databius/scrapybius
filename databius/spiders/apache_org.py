import scrapy
from scrapy_playwright.page import PageMethod

from databius.items import LogoItem

DOWNLOAD_DIR = "./data"


class ApacheOrgSpider(scrapy.Spider):
    name = "apache.org"
    start_url = "https://www.apache.org/logos"

    custom_settings = {
        "ITEM_PIPELINES": {
            "databius.pipelines.SvgPipeline": 1,
        },
        "FILES_STORE": f"{DOWNLOAD_DIR}"
    }

    def start_requests(self):
        yield scrapy.Request(
            self.start_url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        "wait_for_selector",
                        selector='//div[@class="project_rect"]',
                    ),
                    PageMethod("wait_for_load_state", state="networkidle"),
                    PageMethod("wait_for_timeout", 1000),
                ],
                errback=self.errback,
            ),
            callback=self.parse,
        )

    def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        page.close()

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.screenshot(
            path=f"{DOWNLOAD_DIR}/page.png", full_page=True
        )  # Local debug

        print(f"Parsing response...")
        for selector in response.xpath('//div[@class="project_rect"]'):
            base_name = selector.xpath('h4/text()').get()
            ref = selector.xpath('p/a/@href').get()
            for i, logo in enumerate(selector.xpath('div[starts-with(@id,"logo")]')):
                for img in logo.xpath('a'):
                    img_url = img.xpath('@href').get()
                    if str(img_url).endswith(".svg"):
                        name = f"{base_name} v{i + 1}" if i > 0 else base_name
                        yield LogoItem(name=name, ref=ref, file_urls=[img_url])
