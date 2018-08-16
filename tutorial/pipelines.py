# -*- coding: utf-8 -*-
# encoding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class TestPipeline(object):

    def open_spider(self, spider):
        pass
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        print item["name"]
        return item
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('items.jl', 'w',encoding='utf-8' )

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False,indent=2) + "\n"
        self.file.write(line)
        return item