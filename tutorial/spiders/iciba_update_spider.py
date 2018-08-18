# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs, toZh
from pymongo import MongoClient
from ..items import *


class IcibaQuerySpider(scrapy.Spider):
    name = "iciba_update"



    def start_requests(self):


        urls = [
            'http://www.iciba.com/'+'admire'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        # item = response.meta['item']
        base = response.xpath('//div[@class="in-base"]')

        newItem = WordItem()
        # for p in item.keys():
        #     newItem[p] = item[p]
        newItem['word'] = 'admire'
        # ******************
        oral = base.xpath('./div/div/div[@class="base-speak"]/span');
        newItem['en'] = oral[0].xpath('./span/text()').re_first(r'\[(.*)\]')
        newItem['en_video'] = oral[0].xpath('./i/@ms-on-mouseover').re_first(r'\'(.*)\'')

        newItem['am'] = oral[1].xpath('./span/text()').re_first(r'\[(.*)\]')
        newItem['am_video'] = oral[1].xpath('./i/@ms-on-mouseover').re_first(r'\'(.*)\'')

        # newItem['file_urls'] = [newItem['en_video'], newItem['am_video']]



        # ******************
        _changes = base.xpath('./li[contains(@class,"change")]/p/span');
        changeNames = _changes.xpath('./text()').extract()
        changeNames = [x for x in changeNames if x.strip()]
        changeValues = _changes.xpath('./a/text()').extract()
        change = {}
        for index, a in enumerate(changeNames):
            if "复数" in a:
                change['plural'] = changeValues[index].strip()
            elif "过去式" in a:
                change['past_tense'] = changeValues[index].strip()
            elif "过去分词" in a:
                change['past_participle'] = changeValues[index].strip()
            elif "现在分词" in a:
                change['present_participle'] = changeValues[index].strip()
            elif "第三人称单数" in a:
                change['third_person_singular'] = changeValues[index].strip()
        newItem['change'] = change

        yield newItem


