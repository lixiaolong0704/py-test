# -*- coding: utf-8 -*-
# encoding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from utilities import toZh
from pymongo import MongoClient


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class TestPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # print item
        # print item['name']
        # if item['word'] is not None:
        #     print item['word']
        try:
            if item is None:
                return None
            if 'name' in item:
                print item['name']

            if 'word' in item:
                print item['word']

            return item
        except Exception, e:
            print 'fuck le' + str(e)


class MongoWriterPipeline(object):

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection['moli_word']
        self.categories = self.db['categories']
        if self.categories is not None:
            self.categories.remove()

    def process_item(self, item, spider):
        self.categories.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.connection.close()


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
