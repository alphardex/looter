import os
from pprint import pprint
from concurrent import futures
import requests
import looter as lt
import pandas as pd

domain = 'https://unsplash.com'
total = []


def crawl(url):
    imgs = requests.get(url, headers=lt.DEFAULT_HEADERS).json()
    for img in imgs:
        data = {}
        data['created'] = img['created_at']
        data['url'] = img['urls']['full']
        data['likes'] = img['likes']
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/napi/collections/1065976/photos?page={n}&per_page=10&order_by=latest&share_key=a4a197fc196734b74c9d87e48cc86838' for n in range(1, 136)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    lt.save_as_json(total, name='unsplash.json', sort_by='likes', order='desc')
    pd.read_json('unsplash.json', encoding='utf-8').to_csv('unsplash.csv', encoding='utf-8')
    os.remove('unsplash.json')
