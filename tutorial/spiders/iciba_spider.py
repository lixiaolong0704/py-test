# -*- coding: utf-8 -*-
import scrapy
from ..utilities import printhxs
import pinyin
import re

pat = re.compile(r'\s+')


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
        cates = response.xpath('//li/h3/text()').extract()
        for cate in cates:
            printhxs(cate + ":" + pat.sub('', pinyin.get(cate, format="strip", delimiter="").lower()))

        # for index,tr in enumerate(trs):
        #     text = tr.xpath('//td/p/span/text()').extract()
        #     # text= tr.xpath('//td/p/span/text()').extract()
        #     print '******************'
        #     for td in text:
        #          printhxs(td)
        # printhxs(str(text))

        filename = 'word.iciba-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('保存 Saved file %s' % filename)
