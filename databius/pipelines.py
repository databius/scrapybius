# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.pipelines.files import FilesPipeline


class SvgPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_dir = self.spiderinfo.spider.name
        file_dir = f'{file_dir}/{item.get("category")}' if item.get("category") else file_dir
        file_dir = f'{file_dir}/{item.get("sub_category")}' if item.get("sub_category") else file_dir
        return f"{file_dir}/{item['name']}.svg"


class DatabiusPipeline:
    def process_item(self, item, spider):
        return item
