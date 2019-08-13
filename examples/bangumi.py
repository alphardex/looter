"""
bangumi上的追番记录
"""
import os
import json
import re
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'http://bangumi.tv'
user_id = '399538'
page_limit = 4
encoding = 'utf-8'
total = []

format_date = lambda date: '-'.join(f'0{d}' if len(d) == 1 else d for d in re.sub(r'年|月|日', '-', date)[:-1].split('-'))


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('ul#browserItemList li.item')
    for item in items:
        data = {}
        data['title'] = item.css('h3 a.l::text').extract_first()
        data['date'] = format_date(item.css('p.info::text').extract_first().strip().split(r'/')[1].strip())
        data['url'] = f"{domain}{item.css('h3 a.l::attr(href)').extract_first()}"
        pprint(data)
        total.append(data)


def generate():
    with open('bangumi.json', encoding=encoding) as i, open('bangumi.md', 'w', encoding=encoding) as o:
        data = json.loads(i.read())
        o.writelines(f"{i+1}. [{d['title']}]({d['url']}) {d['date']}\n" for i, d in enumerate(data))


if __name__ == '__main__':
    tasklist = [f'{domain}/anime/list/{user_id}/collect?orderby=date&page={n}' for n in range(1, page_limit + 1)]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='bangumi.json', sort_by='date', order='desc')
    generate()
    os.remove('bangumi.json')
