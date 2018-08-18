# -*- coding: utf-8 -*-
import scrapy
from  .. utilities import printhxs

class IcibaQuerySpider(scrapy.Spider):
    name = "iciq"

    def start_requests(self):
        urls = [
            'http://www.iciba.com/need'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        print response.url
 
        
        filename = 'iciba_query_xx.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('保存 Saved file iciba_query_xx %s' % filename)