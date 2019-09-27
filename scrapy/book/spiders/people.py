# -*- coding: utf-8 -*-
import scrapy
from book.items import BookItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    start_urls = ['http://www.rw-cn.com/index.php/category?cid=7&p={}'.format(i) for i in range(0,6749,7)]

    def parse(self, response):
        if 'cid' in response.url:
            urls=response.xpath('//a[@class="a_7 fl"]/@href').extract()
            for url in urls:
                yield scrapy.Request(url)
        elif 'view' in response.url:
            item = BookItem()
            item['name']=response.xpath('//h2[@class="h_10"]/text()').extract()[0].replace('\t', '')
            item['price']=response.xpath('//h2[@class="h_10"]/span/text()').extract()[0]
            item['isbn'] =response.xpath('//div[@class="div_47 fix"]/span/text()').extract()[1].replace('ISBN：','')
            item['url']=response.url
            yield item

