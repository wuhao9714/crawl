# !/usr/bin/env python
# coding:utf-8
# Author: WuHao

from bs4 import BeautifulSoup
import requests
import time

start_time = time.time()
urlmodel = "http://www.rw-cn.com/index.php/category?cid=7&p="
urllist = []

print("正在获取所有图书URL")
for i in range(0, 6749, 7):
    urlcur = urlmodel + str(i)
    f = requests.get(urlcur)  # Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")
    for j in soup.find_all('a', class_='a_7 fl'):
        urllist.append(j['href'])

fd = open('book.txt', 'w', encoding='utf-8')
for i,url in enumerate(urllist):
    print("正在分析第%d页" % i)
    f = requests.get(url)  # Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")  # 用lxml解析器解析该网页的内容, 好像f.text也是返回的html

    for j in soup.find_all('h2', class_='h_10'):
        # print(j.text)
        name=j.text.split()[0]
        price=j.text.split()[1]
        for k in soup.find_all('div', class_='div_47 fix'):  # ,找到div并且class为pl2的标签
            a = k.find_all('span')  # 在每个对应div标签下找span标签，会发现，一个a里面有四组span
            isbn=a[1].text.replace('ISBN：','')
            fd.write('书名：'+name+ '\n')
            fd.write('ISBN号码：' + isbn + '\n')
            fd.write('当前价格：' + price + '\n')
            fd.write('销售网站：' + url+ '\n')
        fd.write('----------------------------------------\n')

fd.close()
end_time=time.time()
print("耗时："+ str(int((end_time-start_time)/60)) + '分' + str(int((end_time-start_time)%60)) + '秒\n')