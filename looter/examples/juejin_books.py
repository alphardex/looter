"""
掘金小册，按购买量排序
"""
import requests
import looter as lt
from pprint import pprint

domain = 'https://juejin.im'
total = []


def crawl(url):
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['d']
    for item in items:
        data = {}
        data['title'] = item['title']
        data['desc'] = item['desc']
        data['author'] = item['userData']['username']
        data['profile'] = item['profile']
        data['buyCount'] = item['buyCount']
        data['price'] = item['price']
        data['publishDate'] = item['finishedAt']
        data['url'] = f"{domain}/book/{item['_id']}"
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'https://xiaoce-timeline-api-ms.juejin.im/v1/getListByLastTime?uid=5901b4faac502e0063cf9e02&client_id=1555503959385&token=eyJhY2Nlc3NfdG9rZW4iOiJuM0g1REUzUUZ0RjczNnJwIiwicmVmcmVzaF90b2tlbiI6InVJck0zcURsbjlkU2dJRm8iLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ%3D%3D&src=web&alias=&pageNum={n}' for n in range(1, 4)]
    [crawl(task) for task in tasklist]
    lt.save(total, name='juejin_books.csv', sort_by='buyCount', order='desc')
