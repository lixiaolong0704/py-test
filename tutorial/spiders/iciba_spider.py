# -*- coding: utf-8 -*-
import scrapy



class IcibaSpider(scrapy.Spider):
    name = "bjh"

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