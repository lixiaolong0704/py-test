# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs
from pymongo import MongoClient
from ..items import *

class IcibaQuerySpider(scrapy.Spider):
    name = "iciq"

    def find_cate(self, cate):
        currentCate = self.db[cate['key']]
        for word in currentCate.find():
            yield scrapy.Request(url='http://www.iciba.com/' + word['word'], meta={'item': word}, callback=self.parse,
                                 dont_filter=True)

    def query_cates(self):
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection['moli_word']
        self.categories = self.db['categories']
        for cate in self.categories.find():

            # level2
            if 'hasChild' in cate:
                if cate['hasChild'] == 0:
                    print cate['name']
                    for x in self.find_cate(cate):
                        yield x
            else:  # level3
                if cate['parent'] != 0:
                    print cate['name']
                    for x in self.find_cate(cate):
                        yield x

    def start_requests(self):
        print '******************** query'
        self.qnext = self.query_cates()
        yield next(self.qnext)

        # urls = [
        #     'http://www.iciba.com/need'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        item = response.meta['item']
        newItem = WordItem()

        for p in item.keys():
            newItem[p] = item[p]


        yield newItem
        if self.qnext is not None:
            yield next(self.qnext)
        # filename = 'iciba_query_xx.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('保存 Saved file iciba_query_xx %s' % filename)
