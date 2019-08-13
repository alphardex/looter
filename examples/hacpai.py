"""
黑客派上“好玩”领域的文章，按阅览数排序
"""
from pprint import pprint
import requests
from parsel import Selector
import looter as lt

domain = 'https://hacpai.com'
total = []
expand_num = lambda num: float(num[:-1]) * 1000 if 'K' in num else int(num)


def crawl(url):
    html = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['contentHTML']
    tree = Selector(text=html)
    items = tree.css('li.article-list__item')
    for item in items:
        data = {}
        data['title'] = item.css('h2 a::text').extract_first()
        data['link'] = item.css('h2 a::attr(href)').extract_first()
        data['views'] = expand_num(item.css('a.article-list__cnt span::text').extract_first().strip())
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/domain/play?ajax=true&p={n}' for n in range(1, 13)]
    [crawl(task) for task in tasklist]
    lt.save(total, name='hacpai.csv', no_duplicate=True, sort_by='views', order='desc')
