# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs, toZh
import pinyin
import re
from ..items import *

pat = re.compile(r'\s+')


# re.sub(r"\b(this|string)\b", r"<markup>\1</markup>", "this is my string")
def getKey(cate):
    tk = pat.sub('', pinyin.get(cate, format="strip", delimiter="").lower())
    return 'key_' + re.sub(r"[^a-zA-Z\d]", '', tk)


class IcibaSpider(scrapy.Spider):
    name = "iciba"

    allowed_domains = ['word.iciba.com']
    def start_requests(self):
        urls = [
            'http://word.iciba.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getClassUrl(self, classId):
        return "?action=courses&classid=" + str(classId)

    def getCourseUrl(self, classId, courseId):
        return "?action=words&class=" + str(classId) + "&course=" + str(courseId)

    def doClass(self,response, item):
        classId =  item['classId']
        courseCount =item['courseCount']
        key = item['key']
        if courseCount is not None:
            for x in range(courseCount):
              yield response.follow(self.getCourseUrl(classId, x+1), callback=self.parseCourse)



    def parseCourse(self,response):
        # filename = 'word.iciba-xx.html'
        # with open(filename, 'wb') as f:
        print '********************************'
        print response.url
        #     f.write(response.body)
        # self.log('test file %s' % filename)
        yield None
    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('----I love you------------------------------------------------')
        # trs = response.xpath('//table[@class="MsoTableGrid"]/tbody/tr')

        # cates = '\n'.join(response.xpath('//li/h3/text()').extract())
        level1Items = []
        allItems = []
        level1 = response.xpath('//div[@class="main_l"]')

        for index, it in enumerate(level1):
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
            yield item
            for it2 in level2:
                cate2 = it2.xpath("./h3/text()").extract_first()
                key2 = getKey(cate2)
                item = CategoryItem()
                item['name'] = cate2
                item['key'] = key2
                item['parent'] = key

                item['hasChild'] = int(it2.xpath("./@has_child").extract_first())
                item['classId'] = it2.xpath("./@class_id").extract_first()

                shit = it2.xpath("./p/text()").extract_first() #261课，5198词
                shits = re.findall(r'\d+', shit)

                item['wordCount'] = int(shits[0])
                item['courseCount'] = int(shits[1])
                if item['hasChild'] == 0:
                    for ttt in self.doClass(response,item):
                            yield ttt
                allItems.append(item)
                yield item
                level3 = it2.xpath('./div[@class="main_l_box"]/ol/li')
                for it3 in level3:
                    cate3 = it3.xpath("./a/h4/text()").extract_first()
                    item = CategoryItem()
                    item['name'] = cate3
                    item['key'] = getKey(cate3)
                    item['parent'] = key2

                    classId = it3.xpath("./@class_id").extract_first()
                    item['classId'] = int(classId)
                    item['tag'] = self.getClassUrl(item['classId'])

                    countBlock = it3.xpath("./a/p/text()").extract()
                    item['wordCount'] = int(re.sub('[^\d]*', '', countBlock[0]))
                    item['courseCount'] = int(re.sub('[^\d]*', '', countBlock[1]))
                    for ttt in self.doClass(response,item):
                        yield ttt
                    allItems.append(item)
                    yield item

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

        # yield allItems
