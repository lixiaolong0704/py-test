# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs, toZh
import pinyin
import re
from ..items import *

pat = re.compile(r'\s+')

# re.sub(r"\b(this|string)\b", r"<markup>\1</markup>", "this is my string")
def getKey(cate):
    tk= pat.sub('', pinyin.get(cate, format="strip", delimiter="").lower())
    return re.sub(r"[^a-zA-Z]",'',tk)


class IcibaSpider(scrapy.Spider):
    name = "iciba"

    def start_requests(self):
        urls = [
            'http://word.iciba.com/?action=index&reselect=y'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('----I love you------------------------------------------------')
        # trs = response.xpath('//table[@class="MsoTableGrid"]/tbody/tr')

        # cates = '\n'.join(response.xpath('//li/h3/text()').extract())
        level1Items = []
        allItems = []
        level1 = response.xpath('//div[@class="main_l"]')

        for index,it in enumerate(level1):
            cate = it.xpath("./h2/text()").extract_first()
            if cate is None:
                continue

            key = getKey(cate)
            item = CategoryItem()
            item['name'] = cate
            item['key'] = key
            item['parent'] = 0
            level1Items.append(item)
            allItems.append(item)
            level2 = it.xpath("./ul/li")

            for it2 in level2:
                cate2 = it2.xpath("./h3/text()").extract_first()
                key2 = getKey(cate2)
                item = CategoryItem()
                item['name'] = cate2
                item['key'] = key2
                item['parent'] = key
                allItems.append(item)
                level3 = it2.xpath('./div[@class="main_l_box"]/ol/li')
                for it3 in level3:
                    cate3 = it3.xpath("./a/h4/text()").extract_first()
                    item = CategoryItem()
                    item['name'] = cate3
                    item['key'] = getKey(cate3)
                    item['parent'] = key2
                    allItems.append(item)

            # level2 = cate.xpath('//li/h3/text()').extract()
            # print level2

        # cates = response.xpath('//li/h3/text()').extract()
        # for cate in cates:
        #     printhxs(cate + ":" + pat.sub('', pinyin.get(cate, format="strip", delimiter="").lower()))

        # for index,tr in enumerate(trs):
        #     text = tr.xpath('//td/p/span/text()').extract()
        #     # text= tr.xpath('//td/p/span/text()').extract()
        #     print '******************'
        #     for td in text:
        #          printhxs(td)
        # printhxs(str(text))

        # filename = 'word.iciba-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('保存 Saved file %s' % filename)

        return allItems
