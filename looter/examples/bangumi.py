import re
import looter as lt
import pymongo
from lxml import etree
from pprint import pprint
from concurrent import futures

domain = 'http://bangumi.tv'
category = ['anime', 'book', 'music', 'game', 'real']
client = pymongo.MongoClient('localhost', 27017)
db = client.bangumi
col = db.data

def crawl(url):
    res = lt.send_request(url)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)
    items = tree.cssselect('ul#browserItemList li')
    for item in items:
        data = dict()
        data['title'] = item.cssselect('a.l')[0].text
        data['detail'] = domain + item.cssselect('a.l')[0].get('href')
        data['info'] = item.cssselect('p.info')[0].text.strip()
        data['rate'] = float(item.cssselect('small.fade')[0].text)
        data['vote'] = int(re.search(r'\d+' ,item.cssselect('.tip_j')[0].text).group())
        data['category'] = res.url.split(r'/')[3]
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/{c}/browser/?sort=rank&page={n}' for n in range(1, 195) for c in category]
    with futures.ThreadPoolExecutor(40) as executor:
        executor.map(crawl, tasklist)
