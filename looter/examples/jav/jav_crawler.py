import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://www.javbus.pw'
client = pymongo.MongoClient()
db = client.jav
col = db.torrents

def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('#waterfall .item')
    for item in items:
        data = dict()
        data['name'] = item.cssselect('img')[0].get('title')
        data['cover'] = item.cssselect('img')[0].get('src')
        data['link'] = item.cssselect('.movie-box')[0].get('href')
        data['bango'] = item.cssselect('date')[0].text
        data['date'] = item.cssselect('date')[1].text
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/page/{i}' for i in range(1, 90)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
