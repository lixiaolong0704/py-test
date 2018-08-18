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
import sys
from scrapy.pipelines.files import FilesPipeline


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MyFilePipeline(FilesPipeline):
    currentItem = None

    def process_item(self, item, spider):
        self.currentItem = item
        return super(MyFilePipeline, self).process_item(item, spider)

    def file_path(self, request, response=None, info=None):
        path = super(MyFilePipeline, self).file_path(request, response, info)
        return path.replace('full', self.currentItem['category'])


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
                # print item['word']
                sys.stdout.write('x****' + item['word'] + '----')
                sys.stdout.flush()

            return item
        except Exception, e:
            print 'fuck le' + str(e)


class UpdateWordPipeline(object):

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection['moli_word']

    def process_item(self, item, spider):

        if item is None:
            return None

        if 'word' in item:
            if 'file_urls' in item:
                item['en_file'] = item['files'][0]
                item['am_file'] = item['files'][1]
            print item['word']
            if 'category' in item:
                wordCollection = self.db[item['category']]
                wordCollection.update_one(
                    {"_id": item['_id']},
                    {"$set":
                        {
                            'en': item['en'],
                            'am': item['am'],
                            'en_video': item['en_video'],
                            'am_video': item['am_video'],
                            'en_file': item['en_file'],
                            'am_file': item['am_file'],
                            'change': item['change'],
                            'version': item['version']
                        }
                    }
                )
        return item

    def close_spider(self, spider):
        self.connection.close()


class MongoWriterPipeline(object):

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection['moli_word']
        self.categories = self.db['categories']
        if self.categories is not None:
            self.categories.remove()

    def process_item(self, item, spider):

        if item is None:
            return None
        if 'name' in item:
            print item['name']
            self.categories.insert(dict(item))
            t = self.db[item['key']]
            if t is not None:
                t.remove()
        if 'word' in item:
            # print item['word']
            sys.stdout.write(item['word'] + ',')
            sys.stdout.flush()
            self.db[item['category']].insert(dict(item))

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
