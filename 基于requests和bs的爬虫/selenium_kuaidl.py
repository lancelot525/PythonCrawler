#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-05-28 22:09
# @Author  : Lancelot
# @File    : selenium_kuaidl.py

'''
selenium模拟浏览器爬虫

爬取快代理：http://www.kuaidaili.com/
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Item(object):
    '''
    我们模拟Scrapy框架
    写一个item类出来，
    用来表示每一个爬到的代理
    '''

    ip = None  # ip地址
    port = None  # 端口
    anonymous = None  # 匿名程度
    type = None  # http or https
    location = None  # 物理地址
    speed = None  # 速度

class GetProxy(object):
    '''
    获取代理的类
    '''

    def __init__(self, starturl):
        '''
        初始化整个类
        '''
        self.starturl = starturl
        self.urls = self.get_urls()
        self.proxylist = self.get_proxy_list(self.urls)
        self.filename = 'proxy.txt'
        self.saveFile(self.filename,self.proxylist)

    def get_urls(self):
        '''
        返回一个代理url的列表
        '''
        urls = []
        for i in range(1,4):
            url = self.starturl+str(i)
            urls.append(url)
        return urls

    def get_proxy_list(self, urls):
        '''
        返回抓取到代理的列表
        整个爬虫的关键
        '''

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 建立浏览器对象 ，通过chromedriver
        browser = webdriver.Chrome(executable_path=r'D:\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
        proxy_list = []

        for url in urls:
            browser.get(url)
            browser.implicitly_wait(3)
            # 找到代理table的位置
            elements = browser.find_elements_by_xpath('//tbody/tr')
            for element in elements:
                item = Item()
                item.ip = element.find_element_by_xpath('./td[1]').text
                item.port = element.find_element_by_xpath('./td[2]').text
                item.anonymous = element.find_element_by_xpath('./td[3]').text
                item.location = element.find_element_by_xpath('./td[4]').text
                item.speed = element.find_element_by_xpath('./td[5]').text
                print(item.ip)
                proxy_list.append(item)

        browser.quit()
        return proxy_list

    def saveFile(self, filename, proxy_list):
            '''
            将爬取到的结果写到本地
            '''
            with open(filename, 'w') as f:
                for item in proxy_list:
                    f.write(item.ip + '\t')
                    f.write(item.port + '\t')
                    f.write(item.anonymous + '\t')
                    f.write(item.location + '\t')
                    f.write(item.speed + '\n\n')

if __name__ == '__main__':
    get = GetProxy('http://www.kuaidaili.com/free/inha/')