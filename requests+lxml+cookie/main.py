# !/usr/bin/env python
# coding:utf-8
# Author: WuHao

import requests
from lxml import etree
import re
import json
import csv
import time
import random

# 获取网页源代码
def get_page(url):
    headers = {
        'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Cookie':'bid=ANgy5smbLqI; douban-fav-remind=1; __yadk_uid=fh7rf8eP4hEcXSh1Oo3VG8xvSIJcYFAJ; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1569508669%2C%22https%3A%2F%2Fblog.csdn.net%2Fwsmrzx%2Farticle%2Fdetails%2F81989366%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.338294878.1560613956.1569223047.1569508669.3; __utmc=30149280; __utmz=30149280.1569508669.3.2.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/wsmrzx/article/details/81989366; __utma=223695111.2041839357.1569223047.1569223047.1569508669.2; __utmc=223695111; __utmb=223695111.0.10.1569508669; __utmz=223695111.1569508669.2.2.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/wsmrzx/article/details/81989366; __utmt=1; dbcl2="204452846:DsaPqv32nQA"; ck=QjDA; push_noty_num=0; push_doumail_num=0; __utmv=30149280.20445; __utmb=30149280.4.10.1569508669; ll="108288"; _pk_id.100001.4cf6=2018d8177b201b96.1569223047.2.1569510457.1569223047.'
    }
    response = requests.get(url=url,headers=headers)
    html = response.text
    return html

# 解析网页源代码，获取下一页链接
def parse4link(html,base_url):
    link = None
    html_elem = etree.HTML(html)
    url = html_elem.xpath('//div[@id="paginator"]/a[@class="next"]/@href')
    if url:
        link = base_url + url[0]
    return link

# 解析网页源代码，获取数据
def parse4data(html):
    html = etree.HTML(html)
    agrees = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[1]/span/text()')
    authods = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/a/text()')
    stars = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/span[2]/@title')
    contents = html.xpath('//div[@class="comment-item"]/div[2]/p/span/text()')
    data = zip(agrees,authods,stars,contents)
    return data

# 打开文件
def openfile(fm):
    fd = None
    if fm == 'txt':
        fd = open('douban_comment.txt','w',encoding='utf-8')
    elif fm == 'json':
        fd = open('douban_comment.json','w',encoding='utf-8')
    elif fm == 'csv':
        fd = open('douban_comment.csv','w',encoding='utf-8')
    return fd

# 将数据保存到文件
def save2file(fm,fd,data):
    if fm == 'txt':
        for item in data:
            fd.write('----------------------------------------\n')
            fd.write('agree：' + str(item[0]) + '\n')
            fd.write('authod：' + str(item[1]) + '\n')
            fd.write('star：' + str(item[2]) + '\n')
            fd.write('content：' + str(item[3]) + '\n')
    if fm == 'json':
        temp = ('agree','authod','star','content')
        for item in data:
            json.dump(dict(zip(temp,item)),fd,ensure_ascii=False)
    if fm == 'csv':
        writer = csv.writer(fd)
        for item in data:
            writer.writerow(item)

# 开始爬取网页
def crawl():
    moveID = input('请输入电影ID：')
    while not re.match(r'\d{8}',moveID):
        moveID = input('输入错误，请重新输入电影ID：')
    base_url = 'https://movie.douban.com/subject/'+ moveID +'/comments'
    fm = input('请输入文件保存格式（txt、json、csv）：')
    while fm!='txt' and fm!='json' and fm!='csv':
        fm = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
    fd = openfile(fm)
    print('开始爬取')
    link = 'https://movie.douban.com/subject/'+ moveID +'/comments?start=0&limit=20&sort=new_score&status=P&percent_type=l'
    while link:
        print('正在爬取 ' + str(link) + ' ......')
        html = get_page(link)
        link = parse4link(html,base_url)
        data = parse4data(html)
        save2file(fm,fd,data)
        time.sleep(random.random())
    fd.close()
    print('结束爬取')

if __name__ == '__main__':
    crawl()
