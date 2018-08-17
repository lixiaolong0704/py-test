import scrapy
from scrapy.spiders import CrawlSpider, Rule
class QuotesSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        urls = [
            'http://word.iciba.com/?action=words&class=268&course=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        

        for text in response.xpath('//a/text()').extract():
            print '---------%s \n', text

        page = response.url.split("/")[-2]
        filename = 'iciba-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)