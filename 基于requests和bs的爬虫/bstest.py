# -*- coding: utf-8 -*-

import bs4

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister one" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister two" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister three" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = bs4.BeautifulSoup(html_doc, 'lxml')

# print('1', soup.title)
# print('2', soup.title.name)
# print('3', soup.title.string)
# print('4', soup.title.parent.name)
# print('5', soup.find(id='link2'))
# print('6', soup.find(id='link2').attrs)
# print('7', soup.find(id='link2')['href'])
list1 = soup.body.contents
print(list1)

# tag = soup.find_all('a')
# for t in tag:
#     print(t)


