import requests
import bs4
from lxml import html

dict1 = {
    'type':'content',
    'q':'python'
    }
heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'}
rsp = requests.get('https://www.zhihu.com/search?type=content&q=python', data=dict1, headers = heads)

# print(r.url)
# print(r.request.headers)
# print('请求的返回状态', r.status_code)
# print('HTTP请求的Headers', r.headers)
# print('从header中猜测的响应的内容编码方式', r.encoding)
print('从内容中分析的编码方式', rsp.apparent_encoding)
# print(r.text)

# html_doc = r.text
# soup = bs4.BeautifulSoup(html_doc)
# print(soup.prettify())
page = rsp.content
root = html.fromstring(page)

first_title = root.xpath('//*[@id="SearchMain"]/div[2]/div/div/div[1]/div/h2/div/a/span/text()[1]')
print(first_title)

