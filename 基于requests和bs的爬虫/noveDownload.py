#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-05-17 6:58
# @Author  : Lancelot
# @File    : noveDownload.py

import requests
import bs4

# 抓取网页内容
def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        # 如果状态码不是200 则应发HTTPError异常
        r.raise_for_status()
        # 设置编码方式，r.apparent_encoding 从响应内容中分析编码方式(较慢)
        r.encoding = r.apparent_encoding
        # r.encoding='utf-8'
        return r.text
    except Exception as err:
        print(err)
        return " ERROR "

# 获取晓说排行榜及其链接
def get_content(url):
    '''
    爬取每一类型小说排行榜，
    按顺序写入文件，
    文件内容为 小说名字+小说链接
    将内容保存到列表
    并且返回一个装满小说url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    main_soup = soup.find(id="main")
    # 获取小说类别列表
    category_list = main_soup.find_all('div', class_='index_toplist mbottom')
    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a') as f:
            f.write("\n小说种类：{} \n".format(name))

        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

    return url_list

# 获取单本小说的所有章节链接
def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：
    并创建小说文件
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text
    with open('./小说/{}.txt'.format(txt_name), "a+") as f:
        f.write('小说标题：{} \n'.format(txt_name))
    for url in lista:
        url_list.append('http://www.qu.la/' + url.a['href'])

    return url_list, txt_name

# 获取单页文章的内容并保存到本地
def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = get_html(url).replace('<br/>', '\n')
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace(
            'chaptererror();', '')
        title = soup.find('title').text

        with open('./小说/{}.txt'.format(txt_name), "a") as f:
            f.write(title + '\n\n')
            f.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')

def main(base_url):
    novel_url_list = get_content(base_url)
    for novel in novel_url_list:
        t = get_txt_url(novel)
        for chapter in t[0]:
            get_one_txt(chapter, t[1])

    print('小说下载完毕！')

base_url = "https://www.qu.la/wanbenxiaoshuo/"

if __name__ == '__main__':
    main(base_url)
