"""
bangumi上的追番记录
"""
import re
from pprint import pprint
from concurrent import futures
import looter as lt

domain = 'http://bangumi.tv'
user_id = '399538'
page_limit = 4
total = []

format_date = lambda date: '-'.join(f'0{d}' if len(d) == 1 else d for d in re.sub(r'年|月|日', '-', date)[:-1].split('-'))


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('ul#browserItemList li.item')
    for item in items:
        data = {}
        data['title'] = item.css('h3 a.l::text').extract_first()
        info = item.css('p.info::text').extract_first().strip()
        date = info.split(r'/')[1].strip() if r'/' in info else info
        data['date'] = format_date(date)
        data['url'] = f"{domain}{item.css('h3 a.l::attr(href)').extract_first()}"
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/anime/list/{user_id}/collect?orderby=date&page={n}' for n in range(1, page_limit + 1)]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='bangumi.csv', sort_by='date', order='desc')
