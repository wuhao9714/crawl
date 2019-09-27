# !/usr/bin/env python
# coding:utf-8
# Author: WuHao

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json
import csv
import time


class PKUSpider():
    def open_file(self):
        self.fm = input('请输入文件保存格式（txt、json、csv）：')
        while self.fm != 'txt' and self.fm != 'json' and self.fm != 'csv':
            self.fm = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
        if self.fm == 'txt':
            self.fd = open('pku.txt', 'w', encoding='utf-8')
        elif self.fm == 'json':
            self.fd = open('pku.json', 'w', encoding='utf-8')
        elif self.fm == 'csv':
            self.fd = open('pku.csv', 'w', encoding='utf-8', newline='')

    def open_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        self.wait = WebDriverWait(self.browser, 5)

    def init_variable(self):
        self.data = zip()
        self.isLast = False

    def parse_page(self):
        try:
            urls = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="text_right someMoreInfo"]/a')))
            urls = [url.get_attribute('href') for url in urls]
            isbns = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="repeatBookInfo"]/div[@class="content_item"]/div[@class="text_right someMoreInfo"]/\
                div/p[2]/span[2]')))
            isbns = [item.text for item in isbns]
            names = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="text_right someMoreInfo"]/a/h2')))
            names = [item.text for item in names]
            prices = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="repeatBookInfo"]/div[@class="content_item"]/div[@class="text_right someMoreInfo"]/div/p[5]/\
                span[2]')))
            prices = [item.text for item in prices]
            # print(type(urls), urls)
            # print(type(isbns),isbns)
            # print(type(names), names)
            # print(type(prices), prices)
            self.data = zip(names, isbns, prices,urls)
        except selenium.common.exceptions.TimeoutException:
            print('parse_page: TimeoutException')
            self.parse_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('parse_page: StaleElementReferenceException')
            self.browser.refresh()

    def turn_page(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and\
             @class="btn-next"]'))).click()
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            self.isLast = True
        except selenium.common.exceptions.TimeoutException:
            print('turn_page: TimeoutException')
            # self.turn_page()
            self.isLast = True
        except selenium.common.exceptions.StaleElementReferenceException:
            print('turn_page: StaleElementReferenceException')
            self.browser.refresh()

    def write_to_file(self):
        if self.fm == 'txt':
            for item in self.data:
                self.fd.write('----------------------------------------\n')
                self.fd.write('书名：' + str(item[0]) + '\n')
                self.fd.write('ISBN号码：' + str(item[1]) + '\n')
                self.fd.write('当前价格：' + str(item[2]) + '\n')
                self.fd.write('销售网站：' + str(item[3]) + '\n')
        if self.fm == 'json':
            temp = ('书名', 'ISBN号码', '当前价格', '销售网站')
            for item in self.data:
                json.dump(dict(zip(temp, item)), self.fd, ensure_ascii=False)
        if self.fm == 'csv':
            writer = csv.writer(self.fd)
            for item in self.data:
                writer.writerow(item)

    def close_file(self):
        self.fd.close()

    def close_browser(self):
        self.browser.quit()

    def crawl(self):
        self.open_file()
        self.open_browser()
        self.init_variable()
        print('开始爬取')
        self.browser.get('http://www.pup.cn/bookList')
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//label[@role="radio" and\
                     @tabindex="0" and @class="el-radio-button"]'))).click()
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="demo-input-suffix full submit_btn"]\
        /button[2]'))).click()
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        count = 0
        while not self.isLast:
            count += 1
            print('正在爬取第 ' + str(count) + ' 页......')
            self.parse_page()
            self.write_to_file()
            self.turn_page()
        self.close_file()
        self.close_browser()
        print('结束爬取')


if __name__ == '__main__':
    spider = PKUSpider()
    spider.crawl()
