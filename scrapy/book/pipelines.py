# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    def process_item(self, item, spider):
        with open("book.txt", 'a',encoding='utf-8') as fp:
            fp.write('书名：'+item['name'] + '\n')
            fp.write('ISBN号码：'+item['isbn'] + '\n')
            fp.write('当前价格：'+item['price']+'\n')
            fp.write('销售网站：' + item['url'] + '\n')
            fp.write('----------------------------------------\n')
