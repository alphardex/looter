import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'http://api.bilibili.com'
client = pymongo.MongoClient()
db = client.bilibili
col = db.video


def crawl(url):
    res = lt.send_request(url)
    data = res.json()
    if data['code'] != 40003:
        pprint(data['data'])
        col.insert(data['data'])


if __name__ == '__main__':
    tasklist = [f'{domain}/archive_stat/stat?aid={n}' for n in range(1, 10000)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
