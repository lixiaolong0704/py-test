# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs, toZh
import pinyin
import re
from ..items import *
import sys

pat = re.compile(r'\s+')

# re.sub(r"\b(this|string)\b", r"<markup>\1</markup>", "this is my string")
def getKey(cate):
    tk = pat.sub('', pinyin.get(cate, format="strip", delimiter="").lower())
    return 'key_' + re.sub(r"[^a-zA-Z\d]", '', tk)


class IcibaSpider(scrapy.Spider):
    name = "iciba_zzz"

    allowed_domains = ['word.iciba.com']

    allitems = []

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

    def doClass(self, response, item):
        classId = item['classId']
        courseCount = item['courseCount']
        key = item['key']
        if courseCount is not None:
            print '********************************' + item['name'] + str(item['classId']) + "---shit 1"
            yield response.follow(self.getCourseUrl(classId, 1), callback=self.parseCourse,
                                  meta={'item': item, 'ccid': 1})

    def parseCourse(self, response):
        # filename = 'word.iciba-xx.html'
        # with open(filename, 'wb') as f:
        try:
            cateItem = response.meta['item']
            # current_course_id = response.meta['currentCourseId']
            # print '********************************' + item['name'] + str(item['classId']) + "---" + str(current_course_id)
            print response.url
            courseId  = response.meta['courseId']

            wordBlocks = response.xpath('//ul[@class="word_main_list"]/li')
            for wordBlock in wordBlocks:
                item = WordItem()
                item['word'] = wordBlock.xpath('./div[@class="word_main_list_w"]/span/@title').extract_first().strip()
                item['en'] =  wordBlock.xpath('./div[@class="word_main_list_y"]/strong/text()').extract_first().strip()
                item['comment'] = wordBlock.xpath('./div[@class="word_main_list_s"]/span/@title').extract_first().strip()
                item['category'] = cateItem['key']
                item['courseId'] = courseId
                yield item

            if self.reqNext is not None:
                yield next(self.reqNext)
        except Exception,e:
            print str(e)
        # if current_course_id <= courseCount:
        #     yield response.follow(self.getCourseUrl(classId, current_course_id + 1), callback=self.parseCourse,
        #                           meta={'item': item, 'trans': trans})

    def printItem(self, item):
        # print 'print:' + item['name']
        pass
    def reqAll(self,response):
        allitems = self.allitems
        for item in allitems:
            classId = item['classId']
            courseCount = item['courseCount']
            # courseCount = 5
            for x in range(courseCount):
                print ' '
                print "category: %-10s courseId: %-4d courseCount: %-4d" % (item['name'],x+1,courseCount)
                print ' '
                yield response.follow(self.getCourseUrl(classId, x + 1), callback=self.parseCourse,
                                      meta={'item': item,'courseId':x+1})

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('----I love you------------------------------------------------')
        # trs = response.xpath('//table[@class="MsoTableGrid"]/tbody/tr')

        # cates = '\n'.join(response.xpath('//li/h3/text()').extract())
        level1 = response.xpath('//div[@class="main_l"]')
        allitems = []
        for index, it in enumerate(level1):
            cate = it.xpath("./h2/text()").extract_first()
            if cate is None:
                continue

            key = getKey(cate)
            item = CategoryItem()
            item['name'] = cate
            item['key'] = key
            item['parent'] = 0
            level2 = it.xpath("./ul/li")
            self.printItem(item)
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

                shit = it2.xpath("./p/text()").extract_first()  # 261课，5198词
                shits = re.findall(r'\d+', shit)
                item['courseCount'] = int(shits[0])
                item['wordCount'] = int(shits[1])
                if item['hasChild'] == 0:
                    allitems.append(item)
                    # for ttt in self.doClass(response,item):
                    #         yield ttt
                self.printItem(item)
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
                    item['wordCount'] = int(re.sub('[^\d]*', '', countBlock[1]))
                    item['courseCount'] = int(re.sub('[^\d]*', '', countBlock[0]))
                    # for ttt in self.doClass(response,item):
                    #     yield ttt
                    allitems.append(item)
                    self.printItem(item)
                    yield item

            # level2 = cate.xpath('//li/h3/text()').extract()
            # print level2

        # for item in allitems:
        self.allitems = allitems

        self.reqNext = self.reqAll(response)
        yield next(self.reqNext)
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
