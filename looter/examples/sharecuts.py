"""
捷径社区的捷径排行榜
"""
from pprint import pprint
import requests
import looter as lt

domain = 'https://sharecuts.cn'
total = []


def crawl(url):
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()
    for item in items:
        data = {}
        data['name'] = item['name']
        data['category'] = item['Category']['name']
        data['note'] = item['note']
        data['author'] = item['User']['nickname']
        data['url'] = item['url']
        data['downloads'] = item['downloads_count']
        data['votes'] = item['votes_count']
        data['comments'] = item['comments_count']
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    task = f'{domain}/api/shortcuts/hot?offset=0&limit=1025'
    crawl(task)
    lt.save(total, name='sharecuts.csv', sort_by='votes', order='desc')
