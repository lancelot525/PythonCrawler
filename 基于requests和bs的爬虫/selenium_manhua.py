#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-05-29 9:03
# @Author  : Lancelot
# @File    : selenium_manhua.py

import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def SavePic(filename, url):
    '''
    通过requests库
    将抓取到的图片保存到本地
    '''
    content = requests.get(url).content
    with open(filename, 'wb') as f:
        f.write(content)

def get_TOF(index_url):
    '''
    获取漫画的目录中的每一章节的url连接
    并返回一个字典类型k：漫画名 v：章节链接
    '''
    url_list = []
    # 模拟浏览器并打开网页
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 建立浏览器对象 ，通过chromedriver
    browser = webdriver.Chrome(executable_path=r'D:\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
    browser.get(index_url)
    browser.implicitly_wait(3)

    # 找到漫画标题 并创建目录
    title = browser.title.split(',')[0]
    mkdir(title)

    # 找到漫画章节，注意，漫画可能会有多种篇章
    # 例如番外，正文，短片等等
    # 找到漫画章节所在的a标签
    comics_lists = browser.find_elements_by_xpath('//div[@class="comic_Serial_list"]/a')

    # 找出具体章节链接
    for a in comics_lists:
        url_list.append(a.get_attribute('href'))

    # 关闭浏览器
    browser.quit()

    Comics = dict(name=title, urls=url_list)

    return Comics

def get_pic(Comics):
    '''
    打开每个章节的url，
    找到漫画图片的地址，
    并写入到本地
    '''
    comic_list = Comics['urls']
    basedir = Comics['name']

    # 模拟浏览器并打开网页
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 建立浏览器对象 ，通过chromedriver
    browser = webdriver.Chrome(executable_path=r'D:\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
    for url in comic_list:
        browser.get(url)
        browser.implicitly_wait(3)

        # 创建章节目录
        dirname = basedir + '/' + browser.title.split('-')[1]
        mkdir(dirname)

        # 找到该漫画一共有多少页
        pageNum = len(browser.find_elements_by_tag_name('option'))

        # 找到下一页的按钮
        nextpage = browser.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        # 找到图片地址，并点击下一页
        for i in range(pageNum):
            pic_url = browser.find_element_by_id('curPic').get_attribute('src')
            filename = dirname + '/' + str(i) + '.png'
            SavePic(filename, pic_url)
            # 点击下一页的按钮，加载下一张图
            nextpage.click()

        print('当前章节\t{}  下载完毕'.format(browser.title))

    browser.quit()
    print('所有章节下载完毕')

def main():
    url = str(input('请输入漫画首页地址： \n'))
    Comics = get_TOF(url)
    get_pic(Comics)

if __name__ == '__main__':
    main()