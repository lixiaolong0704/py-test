# -*- coding: utf-8 -*-
import scrapy

def printhxs(hxs):
    str = ""
    for i in hxs:
        str += i.encode('utf-8')
    print str

class QuotesSpider(scrapy.Spider):
    name = "bjh"

    def start_requests(self):
        urls = [
            'http://bxjg.circ.gov.cn/web/site0/tab5203/info4112314.htm' 
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('----I love you------------------------------------------------')
        trs = response.xpath('//table[@class="MsoTableGrid"]/tbody/tr')

        for index,tr in enumerate(trs):
            text = tr.xpath('//td/p/span/text()').extract()
            # text= tr.xpath('//td/p/span/text()').extract()
            print '******************'
            for td in text:
                 printhxs(td)
            # printhxs(str(text))
 
        
        filename = 'cicr-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('保存 Saved file %s' % filename)