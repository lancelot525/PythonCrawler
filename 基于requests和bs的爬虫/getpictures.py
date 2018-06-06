import requests
from bs4 import BeautifulSoup
import json


#发送请求函数
def getpage(header, cookie):
    for i in range(0,1000):
        base_url = 'https://www.zhihu.com/api/v4/questions/29815334/answers?include=data%5B*%5D.is_normal%2Cadmin_closed' \
                   '_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis' \
                   '_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent&offset=' + str(i) + '&limit=1&sort' \
                 '_by=default'
        response = requests.get(base_url, headers=header, cookies=cookie)
        html = response.text
        img_json = json.loads(html)
        print(base_url)
        print('正在抓取知乎长腿小姐姐图片 第%s条评论'% i)
        contentpage(img_json)
#解析json数据
def contentpage(img_json):
    try:
        data = img_json["data"][0]
        content = data["content"]
        # print(content)
        html = BeautifulSoup(content,'lxml')
        # 提取img标签 由于会抓到两张一页的图片所以每隔一个提取一次
        img_page = html.select('img')[::2]
        for i in img_page:
            address = i.get('src')
            # print(address)
            imgpage(address)
    except:
        print('此评论没有图片')
#存储函数
def imgpage(address):
    #用图片地址后缀当图片名
    fname = address.split('/')[-1]
    response = requests.get(address)
    #直接返回二进制数据
    html = response.content
    with open('./changtui/'+ fname , 'wb') as f:
        f.write(html)


if __name__ == '__main__':
    headers = {
        'Cache-Control': 'max-age=0',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'
                      ' QBCore/3.43.691.400 QQBrowser/9.0.2524.400'
    }
    cookies = {
        #不给你们看
    }
    getpage(headers, cookies)