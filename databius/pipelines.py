# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pathlib

from scrapy.pipelines.files import FilesPipeline


# useful for handling different item types with a single interface


class SvgPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_dir = self.spiderinfo.spider.name
        file_dir = f'{file_dir}/{item.get("category").replace("/", "_")}' if item.get("category") else file_dir
        file_dir = f'{file_dir}/{item.get("sub_category").replace("/", "_")}' if item.get("sub_category") else file_dir

        file_extension = pathlib.Path(item['file_urls'][0]).suffix
        return f"{file_dir}/{item['name']}{file_extension}"


class DatabiusPipeline:
    def process_item(self, item, spider):
        return item
