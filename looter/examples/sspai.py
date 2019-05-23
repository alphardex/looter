"""
少数派的文章，按喜好数排序
"""
import requests
import arrow
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://sspai.com'
total = []


def crawl(url):
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['list']
    for item in items:
        data = {}
        data['title'] = item['title']
        data['released_at'] = arrow.get(item['released_at']).naive
        data['summary'] = item['summary']
        data['words_count'] = item['words_count']
        data['likes_count'] = item['likes_count']
        data['favorites_count'] = item['favorites_count']
        data['comments_count'] = item['comments_count']
        data['url'] = f"{domain}/post/{item['id']}"
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/api/v1/articles?offset={n * 10}&limit=10&type=recommend_to_home&sort=recommend_to_home_at&include_total=false' for n in range(1170)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='sspai.csv', sort_by='likes_count', order='desc')
