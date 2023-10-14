# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

"""
1. 配置过滤少于多少单词。
2. 配置过滤关键词。
3. 配置不过滤带有哪些关键词。
4. 关键词替换。
5. 指定网页过滤。
"""


class GeneralPipeline:
    def process_item(self, item, spider):
        return item


class ConfiguredPipeline:
    def process_item(self, item, spider):
        return item
