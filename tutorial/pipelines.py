# -*- coding: utf-8 -*-
# encoding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from utilities import toZh


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class TestPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('items.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        # x = toZh(json.dumps(dict(item), indent=2))
        # print item["name"]

        line = item["name"] + ":" + item["key"] + "\n"
        self.file.write(line)
        return item
